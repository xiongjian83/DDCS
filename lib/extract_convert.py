import json
import re
from pathlib import Path

from lib.extract_config import config
from lib.extract_config_manually import config_manually

_json_path = Path(__file__).parent.parent / "config.json"
_re_quoted = re.compile(r"""(?<!\\)(['"`])(.*?)(?<!\\)\1""")
_re_text_vars = re.compile("\{\d+}")


def extract_qstr(string):
    find = _re_quoted.findall(string)
    if find:
        return [v[1] for v in find]
    if string[0] == "`":
        string = string[1:]
    if string[-1] == "`":
        string = string[:-1]
    return [string]


def convert_from_json():
    """
    尽量将原有 config.json 中的值提取出来, 判断是否在 extract_config 中
    """
    config_set = set(s.strip() for src, dst in config if dst != "" for s in _re_text_vars.split(src))
    config_set.update(s.strip() for src, _ in config_manually for s in extract_qstr(src))

    with open(_json_path, "r", encoding="utf-8") as reader:
        json_config = json.loads(reader.read())["all"]
    for v in json_config:
        for src, dst in zip(extract_qstr(v["src"]), extract_qstr(v["dest"])):
            if src != dst and src.strip() not in config_set:
                print(src, dst)


if __name__ == "__main__":
    convert_from_json()
