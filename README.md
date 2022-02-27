# txt-cli

The CLI tool for https://github.com/ahui2016/txt


## Install (安装)

txt-cli 使用了 Python 3.10 的新特性，比如 type union operator, 因此，如果你的系统中未安装 Python 3.10, 推荐使用 [pyenv](https://github.com/pyenv/pyenv) 或 [miniconda](https://docs.conda.io/en/latest/miniconda.html) 来安装最新版本的 Python。


### 简单安装方法

执行以下命令即可：

```sh
pip install txtcli
```

升级：

```sh
pip install -U txtcli
```

### 另一种安装方法

另外，还可以使用 pipx 来安装, pipx 会自动为 txt-cli 创建一个虚拟环境，不会污染系统环境，并且使用时不用管理虚拟环境。推荐大家多了解一下 pipx。

pipx 的介绍及安装方法: https://pypa.github.io/pipx/ 安装 pipx 后执行以下命令即可：

```sh
pipx install txtcli
```

升级：

```sh
pipx upgrade txtcli
```

### Server and the secret-key (服务器地址与密钥)

- 安装后，默认已设置了演示版的服务器地址，可使用命令 `txt getkey`, 输入主密码(abc) 即可获取日常操作密钥。
- 执行 `txt getkey` 后如无错误，即可正常使用。
- 如果密钥过期，可使用命令 `txt getkey -gen` 生产新密钥。
- 如果你有自己的服务器，可使用命令 `txt server -set [url]` 修改服务器地址。


## Features (功能)

### 基本功能

- `txt` 列出最近 5 条暂存消息
- `txt next` 列出后续 5 条消息（暂时不做这个功能）
- `txt get [index/alias]` 通过 index 或别名获取(复制，同时打印到屏幕)一条消息，默认获取 T1
- `txt send [message]` 发送消息 (添加暂存消息)
- `txt toggle [index/alias]` 切换一条消息的类型(暂存/永久), 默认把 T1 切换为 P1
- `txt list -n 3` 列出最近 3 条暂存消息（默认 n = 9）
- `txt list p1` 列出最近 n 条永久消息（默认 n = 9）
- `txt list p3 -n 7` 从第 3 条永久消息开始，列出 5 条永久消息
- `txt list --alias` 列出全部别名
- `txt alias [index/alias] [alias]` 设置或删除别名
- `txt delete [index/alias]` 删除一条消息
- `txt search [keyword]` 查找消息

### 其他功能

- `txt getkey` 获取密钥（同时提示密钥状态），需要输入主密码
- `txt getkey -gen/--generate` 生产新密钥，需要输入主密码
- `txt changepwd` 更改主密码 (暂时不做这个功能)
- `txt server` 查看当前服务器地址
- `txt server -set [url]` 修改服务器地址

其中，`index` 是消息的流水号，每当添加消息、删除消息、转换状态时都会导致流水号发生变化，以 T 开头的流水号表示暂存消息，以 P 开头表示永久消息，比如 `T1` 表示最新一条暂存消息, `P3` 表示第 3 条永久消息，其中 T/P 不分大小写。

`alias` 是消息的别名，一个别名只能对应一条消息。不可采用“以 T 或 P 开头紧跟数字”的形式（要避免与 index 冲突）。

### Help (帮助)

- `txt -h` （命令列表）
- `txt getkey -h` （每个子命令都有帮助信息）

### 复制失败

复制到剪贴板的功能由 pyperclip 实现，如果复制失败，请看这里 [https://pyperclip.readthedocs.io/en/latest/#not-implemented-error](https://pyperclip.readthedocs.io/en/latest/#not-implemented-error)
