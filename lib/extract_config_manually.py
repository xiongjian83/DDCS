"""
一些文本无法被识别, 手动添加, 应当直接 replace

1. children 中参与拼接的表达式文本
2. 不以 _re_text 中常规前缀开头, 存储在变量中的文本
"""

config_manually = [
    # ==============================# & | 表达式 #==============================#
    (
        '__DARWIN__&&" The configurations below can be changed later in Settings."',
        '__DARWIN__&&" 下面的配置可以稍后在设置中更改。"',
    ),
    ('__DARWIN__?"Settings...":"Change settings"', '__DARWIN__?"设置...":"修改设置"'),
    ('&&" & restart"', '&&"并重启"'),
    ('&&" See full image description below to learn more."', '&&" 请参阅下面完整镜像说明以了解更多信息。"'),
    ('&&"Your legacy Docker Scout plan is no longer available. "', '&&"你之前的 Docker Scout 计划不再可用。"'),
    ("&&` - ${_.length} selected`", "&&` - ${_.length} 已选择`"),
    ('||"Loading..."', '||"加载中..."'),
    # ==============================#  三目运算符 #==============================#
    (
        'S.wslPreconditionMessage?`Use the WSL 2 based engine (${S.wslPreconditionMessage})`:"Use the WSL 2 based engine"',
        'S.wslPreconditionMessage?`使用基于 WSL 2 的引擎 (${S.wslPreconditionMessage})`:"使用基于 WSL 2 的引擎"',
    ),
    (
        'label:d?"Only running":l?"Running":"Only show running containers"',
        'label:d?"仅运行中":l?"运行中":"仅显示正在运行的容器"',
    ),
    ('1===t?"item":"items"', '"项目"'),
    ('w?void 0:"No recommendation available at this time."', 'w?void 0:"目前没有可用的建议。"'),
    ('?"existing":"new"', '?"现有":"新的"'),
    ('?"install":"download"', '?"安装":"下载"'),
    ('?"has been":"will be"', '?"已经":"将要"'),
    ('?"less than a minute ago":`${A} minutes ago`', '?"于一分钟以内":`于 ${A} 分钟前`'),
    ('?"less than a minute ago":`${Z} minutes ago`', '?"于一分钟以内":`于 ${Z} 分钟前`'),
    ('?"running":""', '?"运行中":""'),
    ('?" (not found)":" (unknown error)"', '?"（未找到）":"（未知错误）"'),
    ('?"unlimited":', '?"无限制":'),
    ('?"default: 192.168.65.0/24":"Invalid value"', '?"默认: 192.168.65.0/24":"无效值"'),
    ('?"Collapse All":"Expand All"', '?"折叠所有":"展开所有"'),
    ('?"Contact your admin":"Go to the Dashboard"', '?"联系你的管理员":"打开面板"'),
    ('?"Starting":"Resume"', '?"启动中":"恢复"'),
    ('?"Start a container to exit this mode":null', '?"启动容器即可退出该模式":null'),
    ('?r:"Sign in / Sign up"', '?r:"登录 / 注册"'),
    ('?"Pausing":"Pause"', '?"暂停中":"暂停"'),
    ('?"Starting ...":"Stopping ..."', '?"启动中 ...":"停止中 ..."'),
    ('?`Verifying credentials for ${M}`:"Processing login data..."', '?`正在验证 ${M}`:"正在处理登录数据..."'),
    ('?"Copied to clipboard":"Copy docker run"', '?"已复制到剪贴板":"复制运行命令"'),
    ('?"Push to Docker Hub":"Push"', '?"推送到 Docker Hub":"推送"'),
    ('?"Full history supported":"History not supported"', '?"支持完整历史记录":"不支持历史记录"'),
    ('?"Multi-platform ready":"Single platform"', '?"多平台":"单平台"'),
    ('?"Hide timestamps":"Show timestamps"', '?"隐藏时间戳":"显示时间戳"'),
    ('?"Deleting...":"Delete forever"', '?"删除中...":"永久删除"'),
    ('?"In use":"Not in use"', '?"使用中":"未使用"'),
    ('?"Copied to clipboard!":"Copy to clipboard"', '?"已复制到剪贴板":"复制到剪贴板"'),
    ('?"Debug":"Exec"', '?"调试":"运行"'),
    ('?"Error":"Source"', '?"错误":"源"'),
    ('?"Hide file editor":"Open file editor"', '?"隐藏文件编辑器":"打开文件编辑器"'),
    ('?"":"Undo changes"', '?"":"撤销更改"'),
    ('?"":"Redo changes"', '?"":"重做更改"'),
    ('?"Save changes":""', '?"保存更改":""'),
    ('?"Install anyway":"Install"', '?"始终安装":"安装"'),
    ('?"Version":"Latest version"', '?"版本":"最新版本"'),
    # ==============================# 变量中 #==============================#
    ('{work:"Work",personal:"Personal"}', '{work:"商业",personal:"个人"}'),
    ('columnMenuLabel:"Menu"', 'columnMenuLabel:"菜单"'),
    ('columnMenuSortAsc:"Sort by ASC"', 'columnMenuSortAsc:"升序排列"'),
    ('columnMenuSortDesc:"Sort by DESC"', 'columnMenuSortDesc:"降序排列"'),
    ('columnMenuUnsort:"Unsort"', 'columnMenuUnsort:"取消排序"'),
    ('pinToLeft:"Pin to left"', 'pinToLeft:"固定到左侧"'),
    ('pinToRight:"Pin to right"', 'pinToRight:"固定到右侧"'),
    ('unpin:"Unpin"', 'unpin:"取消固定"'),
    ('columnMenuHideColumn:"Hide column"', 'columnMenuHideColumn:"隐藏列"'),
    ('columnMenuManageColumns:"Manage columns"', 'columnMenuManageColumns:"管理列"'),
    ('children:"to open"', 'children:"打开"'),
    ('children:"to navigate"', 'children:"导航"'),
    ('children:"to close"', 'children:"关闭"'),
    ('children:"for more results"', 'children:"更多结果"'),
    ('{inUse:"In use",unused:"Unused",dangling:"Dangling"}', '{inUse:"使用中",unused:"未使用",dangling:"悬空"}'),
    ('{inUse:"In use",unused:"Unused"}', '{inUse:"使用中",unused:"未使用"}'),
    (
        '["To access the latest features, {link}","{link} to use additional features enabled by your organization.","You can do more when you {link}."]',
        '["要访问最新功能，{link}","{link}以使用你组织所启用的附加功能。","{link} 后你可以做更多的事情。"]',
    ),
    ('"Build container images and artifacts from source code."', '"从源代码构建容器镜像和工件。"'),
    ('"Running in Resource Saver mode"', '"资源节省模式运行中"'),
    ('"Docker Desktop failed to start"', '"Docker Desktop 启动失败"'),
    ('"Docker Desktop is paused"', '"Docker Desktop 已暂停"'),
    ('"Docker Desktop is blocked"', '"Docker Desktop 已被阻止启动"'),
    ("`You're now signed in as ${M}`", "`你已登录为 ${M}`"),
    ('"You are signed out"', '"你已经注销"'),
    ('"You must initialize pass before logging in to Docker Desktop"', '"登录之前必须初始化密码"'),
    ('"Sign in to share images and collaborate with your team"', '"登录后可以共享镜像并进行团队协作"'),
    ('"Just now"', '"刚刚"'),
    (
        '" Easily convert your Compose configuration to Kubernetes resources"',
        '" 将您的 Compose 配置轻松转换为 Kubernetes 资源"',
    ),
    ('"Rows per page:"', '"每页条数:"'),
    ('"Repositories per page"', '"每页存储库数:"'),
    (
        '"% of available CPU currently in use by containers. For example, with 4 available CPUs, the CPU usage can be up to 400%. Note that Docker will use some of the remaining CPU for system services like networking."',
        '"容器当前的 CPU 占用。例如，在4个可用 CPU 的情况下，CPU 使用率可高达 400%。请注意，Docker 将使用一些剩余的 CPU 用于系统服务，如网络。"',
    ),
    (
        '"Total amount of memory consumed by running container processes. Note that Docker will use available free memory for caching but this cache will be released when memory is needed by containers."',
        '"运行容器进程的内存占用。请注意，Docker 将使用一些空闲内存进行缓存，但是当容器需要时，此缓存将被释放。"',
    ),
    ('"To execute commands, run the container."', '"要执行命令，请运行容器。"'),
    (
        '"By selecting **accept**, you agree to the [Subscription Service Agreement](https://dockr.ly/3jixb1E), the [Docker Data Processing Agreement](https://dockr.ly/3QLGBBf), and the [Data Privacy Policy](https://dockr.ly/3pFD7En).\\n\\nCommercial use of Docker Desktop at a company of more than 250 employees OR more than $10 million in annual revenue requires a paid subscription (Pro, Team, or Business). [See subscription details](https://dockr.ly/3QOpe2s)\\n"',
        '"通过选择 **接受**, 表示你同意 [订阅服务协议](https://dockr.ly/3jixb1E)，[Docker 数据处理协议](https://dockr.ly/3QLGBBf)，和 [数据隐私协议](https://dockr.ly/3pFD7En).\\n\\n超过 250 名员工或年收入超过 1000 万美元的企业, Docker Desktop 的商业用途需要付费订阅（Pro，Team，或 Business）。[查看订阅详细信息](https://dockr.ly/3QOpe2s)\\n"',
    ),
    ('"Start selected items"', '"启动所选项"'),
    ('"Pause selected items"', '"暂停所选项"'),
    ('"Stop selected items"', '"停止所选项"'),
    (
        '"This image has not been analyzed or does not have a base image. Unable to provide recommendations."',
        '"此镜像尚未分析或没有基础镜像。无法提供建议。"',
    ),
    (
        '"This image is not associated with a tag. Unable to provide recommendations."',
        '"此镜像没有关联的标签。无法提供建议。"',
    ),
    ('"No recommendations available at this time."', '"目前没有可用的建议。"'),
    ('"Sign in to view image recommendations."', '"登录以查看镜像推荐。"'),
    ('"Not reviewed"', '"未审核"'),
    (
        '"This extension has been auto-published to the marketplace and no review was carried out by Docker."',
        '"此扩展已自动发布到市场，Docker 没有进行审核。"',
    ),
    ('"Reviewed"', '"已审核"'),
    (
        '"This extension meets the minimum design and functional requirements advised by Docker."',
        '"此扩展满足 Docker 建议的最低设计和功能要求。"',
    ),
    (
        "`Volume ${t.payload.volumeName} is in use. Delete the container that's using it and try again.`",
        "`卷 ${t.payload.volumeName} 正在使用中。删除正在使用它的容器，然后重试。`",
    ),
    (
        "`Volume ${e.payload.volumeName} is in use. Delete the container that's using it and try again.`",
        "`卷 ${e.payload.volumeName} 正在使用中。删除正在使用它的容器，然后重试。`",
    ),
    (
        '''(t.payload.imageRef?`Image ${t.payload.imageRef}`:"Image")+" is in use. Delete the container that's using it and try again."''',
        '''(t.payload.imageRef?`镜像 ${t.payload.imageRef}`:"镜像")+" 正在使用中。删除正在使用它的容器，然后重试。"''',
    ),
    (
        '''(e.payload.imageRef?`Image ${e.payload.imageRef}`:"Image")+" is in use. Delete the container that's using it and try again."''',
        '''(e.payload.imageRef?`镜像 ${e.payload.imageRef}`:"镜像")+" 正在使用中。删除正在使用它的容器，然后重试。"''',
    ),
    ('''return"You're up to date"''', '''return"当前是最新版"'''),
]
