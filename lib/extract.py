import re
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import List, Tuple, Generator, Union

import black

from common import log
from lib.extract_config import config
from lib.extract_config_manually import config_manually

config_dict = dict(config)

_re_text_vars = re.compile("(\{\d+})")
# 捕获组需要包含 [], 以找到正确的字符串结尾
"""
_re_children_1_external 寻找第一个 child 为英文文本(大写开头)的 children, 例如:
children:["Settings",(0,N.jsx)(U.A,{feedbackUrl:ne,sourcePage:"settings"})]
_re_children_1_external 也允许第一个 child 为空, 第二个 child 为英文文本(大写开头), 例如:
children:[" ","If the error persists, please",...]
"""
_re_children_1_external = re.compile(r"""children:(\[(?:" ",)?(?<!\\)(['"`])[A-Z].*?(?<!\\)\2.*?])""")
"""
_re_children_1_internal 寻找嵌套 children 中的 children, 与 _re_children_1 类似但不要求大写开头
"""
_re_children_1_internal = re.compile(r"""children:(\[(?:" ",)?(?<!\\)(['"`])([a-zA-Z].*?)(?<!\\)\2.*?])""")
"""
_re_children_2_external 寻找最后一个 child 为字符串的 children, 同时排除 _re_children_1, 例如:
children:[(0,B.jsx)(ke.A,{fontSize:"xs",sx:{marginRight:"4px"}}),"Installing update..."]
"""
_re_children_2_external = re.compile(r'children:(\[(?!"[A-Z])[^\[\]]*?,"[^\[\]]*?"])')
"""
_re_nested_children_text 寻找嵌套 children 中的字符串, 理论上属于父级 text 的一部分, 因此不限制大写开头. 例如:
children:[..., children:"contact your administrator", ...]
"""
_re_nested_children_text = re.compile(r'children:"(.*?[a-zA-Z]+?.*?)"')
"""
_re_text 寻找指定 tag 的英文文本(大写开头), 例如:
label:"Docker Home"
children:`Last refresh: ${l}`
"""
_re_text = re.compile(
    r"""(label|title|content|secondary|description|placeholder|children|reason|buttonTitle|helperText|message|detail|checkboxLabel|caption|alt|headerName|tooltip|primary|notificationTitle|warningText):(?<!\\)(['"`])([A-Z].*?)(?<!\\)\2"""
)
"""
_re_array_text 寻找指定 tag 的数组文本 (",messages"是为了干掉 AI 提示词), 例如: 
,messages:[`${o.path} already exists.`,"Please remove it and retry."]
buttons:["Switch","Cancel"]
"""
_re_array_text = re.compile(r'(,messages|buttons):(\[["`].+?["`]])')
"""
_re_children_all_lower_text 判断 children 是否为纯小写文本 (由 _re_children_2_external 提取), 这种情况应该走 array text, 例如:
head:{children:["title","base","link","style","meta","script","noscript","command"]}
"""
_re_children_all_lower_text = re.compile(r'children:\["[a-z]+"(?:,"[a-z]+")+]')


@dataclass
class Text:
    """
    对于简单文本: fmt='label:"{}"', src='Close', dst='关闭', args=None.
    对于 children:
        fmt='children:[{}]',
        src="The {0} element...",
        dst="该 {0} 元素...",
        raw='"The ",(0,y.jsx)("strong",{children:"volumes"}),' element...''
        args=['(0,y.jsx)("strong",{children:"volumes"})'],
        args_len=40,
    """

    start: int
    fmt: str  # label:"{}"
    src: Union[str, List[str]]  # Close
    dst: Union[str, List[str]]  # 关闭
    """children"""
    raw: str = None
    args: List[str] = None
    args_len: int = 0

    def _format_args(self, value: str) -> str:
        rst, accessed = [], [False] * len(self.args)
        for part in _re_text_vars.split(value):
            if not part:
                continue
            if _re_text_vars.match(part):
                idx = int(part[1:-1])
                value, accessed[idx] = self.args[idx], True
            elif '"' in part:
                value = f"'{part}'"
            else:
                value = f'"{part}"'
            rst.append(value)
        not_accessed = [f"{{{idx}}}" for idx, v in enumerate(accessed) if not v]
        if not_accessed:
            log.warn(f"翻译文本中缺少变量值: {','.join(not_accessed)}, 文本: {self.dst}")
        return f'[{",".join(rst)}]'

    def config(self):
        """
        获取配置文件中的字符串元组
        :return: (src, dst), src 是英文文本, dst 是中文文本, 其中 children src 已优化
        """
        if isinstance(self.src, list):
            for src, dst in zip(self.src, self.dst):
                yield src, dst
        else:
            yield self.src, self.dst

    def format(self) -> Tuple[str, str]:
        """
        获取格式化之后的字符串元组
        :return: (src, dst), src 是原始文件中的字符串, dst 是替换后的字符串
        """
        if self.raw:
            return self.fmt.format(self.raw), self.fmt.format(self._format_args(self.dst))
        elif isinstance(self.src, list):
            return self.fmt.format(*self.src), self.fmt.format(*self.dst)
        else:
            return self.fmt.format(self.src), self.fmt.format(self.dst)


def extract(code: str) -> Generator[Text, None, None]:
    """
    extract 使用正则从代码段中提取文本, 并进行进一步解析
    :param code: 代码段
    """
    yield from extract_children(code)
    # extract array
    for match in _re_array_text.finditer(code):
        prefix, src = match.groups()
        yield from _extract_array(prefix, src, match.start())
    # extract text
    for match in _re_text.finditer(code):
        start = match.start()
        fmt, sep, src = match.groups()
        fmt += ":" + sep + "{}" + sep
        dst = config_dict.get(src, "")
        yield Text(start=start, fmt=fmt, src=src, dst=dst)


def extract_children(code: str, code_start: int = 0, nested: bool = False) -> Generator[Text, None, None]:
    """
    extract_children 使用正则从代码段中提取 children 内容, 并进行进一步解析
    :param code: 代码段
    :param code_start: 代码段起始位置
    :param nested: code 代码段是否是 children 代码段, 即当前提取是否为嵌套 children.
    """
    _re_children_1 = _re_children_1_internal if nested else _re_children_1_external
    for match in _re_children_1.finditer(code):
        start = match.start()
        src = match.groups()[0]
        rc = src.count("[")
        if rc > 1:
            start, end = match.span(1)
            while rc > 1:
                if code[end] == "[":
                    rc += 1
                elif code[end] == "]":
                    rc -= 1
                end += 1
            src = code[start:end]
        yield from _extract_children(src, code_start + start)

    if not nested:
        for match in _re_children_2_external.finditer(code):
            if _re_children_all_lower_text.match(match.group()):
                yield from _extract_array("children", match.group()[0], match.start())
            else:
                yield from _extract_children(match.groups()[0], code_start + match.start())


def _extract_children(children_code: str, children_start: int = 0) -> Generator[Text, None, None]:
    """
    _extract_children 将 children 内容切割为 list, 文本存储在 src, 代码段存储在 args, 之后嵌套解析 args
    :param children_code: children 代码段, children:[...]
    :param children_start: 代码段起始位置
    """
    src, group, args, args_len = [], 0, [], 0
    for code, start, is_str in _split_array(children_code):
        if is_str:
            src.append(code[1:-1])
            continue

        src.append(f"{{{group}}}")
        group += 1

        start += children_start
        yield from extract_children(code, start, True)
        # 文本
        for match in _re_nested_children_text.finditer(code):
            text_fmt = 'children:"{}"'
            text_src = match.groups()[0]
            text_dst = config_dict.get(text_src, "")
            yield Text(start=start, fmt=text_fmt, src=text_src, dst=text_dst)
        args.append(code)
        args_len += len(code)
    src = "".join(src)
    yield Text(
        start=children_start,
        fmt="children:{}",
        src=src,
        dst=config_dict.get(src, ""),
        raw=children_code,
        args=args,
        args_len=args_len,
    )


def _extract_array(prefix: str, array_code: str, array_start: int = 0) -> Generator[Text, None, None]:
    fmt, src = prefix + ":[", []
    for code, _, is_str in _split_array(array_code):
        if not is_str:
            return
        fmt += f"{code[0]}{{}}{code[0]},"
        src.append(code[1:-1])
    if src:
        yield Text(start=array_start, fmt=fmt[:-1] + "]", src=src, dst=[config_dict.get(v, "") for v in src])


def _split_array(array_code: str) -> Generator[Tuple[str, int, bool], None, None]:
    """
    将 array 代码段切割为 list
    :param array_code: array 代码段
    """
    array_code = array_code[1:-1]  # unwrap []
    start, dep, in_str = 0, 0, None
    for i, c in enumerate(array_code):
        if c in ("[", "(", "{") and in_str is None:
            dep += 1
        elif c in ("]", ")", "}") and in_str is None:
            dep -= 1
        elif c in ('"', "'"):
            if in_str is None:
                in_str = c
            elif in_str == c:
                in_str = None
        elif c == "," and dep == 0 and in_str is None:
            code = array_code[start:i]
            if not code:
                continue
            yield code, start, code[0] in ('"', "'", "`") and code[0] not in code[1:-1]
            start = i + 1
    code = array_code[start:]
    if not code:
        return
    yield code, start, code[0] in ('"', "'", "`") and code[0] not in code[1:-1]


def files(path: Path):
    for file in path.rglob("main.js"):
        yield file
    for file in path.rglob("*js"):
        if file.name == "main.js":
            continue
        yield file


def generate_config(path: Path, include_old: bool = True, output: str = "extract_config.py"):
    new_config = {}
    for file in files(path):
        with open(file, "r", encoding="utf-8") as reader:
            content = reader.read()
        for text in sorted(extract(content), key=lambda v: v.start):
            new_config.update(text.config())

    buf = StringIO()
    buf.write("config = [\n")
    count = 0
    for item in new_config.items():
        if item[0] not in config_dict:
            count += 1
        buf.write(str(item))
        buf.write(",\n")
    if include_old:
        buf.write("# ==============================# old #==============================#\n")
        for item in config_dict.items():
            src, dst = item
            if src not in new_config and dst != "":
                buf.write(str(item))
                buf.write(",\n")
    buf.write("]\n")

    fmt_content = black.format_str(buf.getvalue(), mode=black.Mode(line_length=120))
    with open(Path(__file__).parent / output, "w", encoding="utf-8") as writer:
        writer.write(fmt_content)

    log.info(
        f"新增个数: {count}, 汉化进度: {sum(1 for v in new_config.values() if v != '') * 100 / len(new_config):.2f} %"
    )


def replace(path: Path):
    used = {}
    for file in files(path):
        with open(file, "r", encoding="utf-8") as reader:
            content = reader.read()
        # 优先替换 args_len 长的, 否则内部嵌套 children 被替换后, 外部 children 将无法替换
        for text in sorted(extract(content), key=lambda v: (-v.args_len, v.start)):
            if text.dst is None or text.dst == "":
                continue
            src, dst = text.format()
            new_content = content.replace(src, dst)
            if new_content != content:
                used.update(text.config())
            content = new_content

        for src, dst in config_manually:
            content = content.replace(src, dst)

        with open(file, "w", encoding="utf-8") as writer:
            writer.write(content)
    for src, dst in config_dict.items():
        if dst is not None and dst != "" and src not in used:
            log.warn(f"unused: {src}")
