# txt-cli

The CLI tool for <https://github.com/ahui2016/txt>


## Install (安装)

txt-cli 使用了 Python 3.10 的新特性，比如 type union operator, 因此，如果你的系统中未安装 Python 3.10, 推荐使用 [pyenv](https://github.com/pyenv/pyenv) 或 [miniconda](https://docs.conda.io/en/latest/miniconda.html) 来安装最新版本的 Python。

例如，安装 miniconda 后，可以这样创建 3.10 环境：

```sh
$ conda create --name py310 python=3.10.4
$ conda activate py310
```

### 简单安装方法

执行以下命令即可：

```sh
pip install txtcli
```

升级：

```sh
pip install -U txtcli
```

### Server and the secret-key (服务器地址与密钥)

- 安装后，默认已设置了演示版的服务器地址，可使用命令 `txt getkey`, 输入主密码(abc) 即可获取日常操作密钥。
- 执行 `txt getkey` 后如无错误，即可正常使用。
- 如果密钥过期，可使用命令 `txt getkey -gen` 生产新密钥。
- 如果你有自己的服务器，可使用命令 `txt server -set [url]` 修改服务器地址。
- 注意：使用密码 abc 连接自带的演示版服务器，只是演示用途，正式使用时你还需要安装这个 → <https://github.com/ahui2016/txt>


## Features (功能)

### 基本功能

- `txt send [message]` 发送消息 (添加暂存消息)
- `txt send` 默认发送系统剪贴板的内容
- `txt send -g` 打开 GUI 窗口发送消息
- `txt send -f ./file.txt` 发送文件内容
- `txt toggle [index/alias]` 切换一条消息的类型(暂存/永久), 默认把 T1 切换为 P1

- `txt` 相当于 'txt list'
- `txt list` 列出最近几条暂存消息
- `txt list -n 3` 列出最近 3 条暂存消息（默认 n = 9）
- `txt list p1` 列出最近 n 条永久消息（默认 n = 9）
- `txt list p3 -n 7` 从第 3 条永久消息开始，列出 5 条永久消息
- `txt get [index/alias]` 通过 index 或别名获取(复制，同时打印到屏幕)一条消息，默认获取 T1

- `txt list -a/--alias` 列出全部别名
- `txt alias -l/--list` 列出全部别名
- `txt alias [index/alias] [alias]` 设置或删除别名
- `txt delete [index/alias]` 删除一条消息
- `txt search [keyword]` 查找消息

### 其他功能

- `txt getkey` 获取密钥（同时提示密钥状态），需要输入主密码
- `txt getkey -gen/--generate` 生产新密钥，需要输入主密码
- `txt getkey -forget` 清除密钥（需要重新获取密钥才能正常使用）
- `txt changepwd` 更改主密码 (暂时不做这个功能)
- `txt server` 查看当前服务器地址
- `txt server -set [url]` 修改服务器地址

其中，`index` 是消息的流水号，每当添加消息、删除消息、转换状态时都会导致流水号发生变化，以 T 开头的流水号表示暂存消息，以 P 开头表示永久消息，比如 `T1` 表示最新一条暂存消息, `P3` 表示第 3 条永久消息，其中 T/P 不分大小写。

`alias` 是消息的别名，一个别名只能对应一条消息。不可采用“以 T 或 P 开头紧跟数字”的形式（为了避免与 index 冲突）。

### Help (帮助)

- `txt -h` （命令列表）
- `txt getkey -h` （每个子命令都有帮助信息）

### 复制失败

复制到剪贴板的功能由 pyperclip 实现，如果复制失败，请看这里 [https://pyperclip.readthedocs.io/en/latest/#not-implemented-error](https://pyperclip.readthedocs.io/en/latest/#not-implemented-error)


## 一个技巧

- `txt get` 可以获取最新一条消息，假设其内容是 "ls -lh", 那么，使用 `bash <(txt get)` 的形式可以执行命令 "ls -lh"
- 一般先执行 `txt get`, 检查内容没问题后再执行 `bash <(txt get)`, 可以避免复制黏贴的麻烦。
- 另外，使用 `txt get > aaa.txt` 的方式可以把内容写到一个文本文件中。


## 更新日志

### v0.1.2

- **add** `txt alias -l/--list` 列出全部别名

### v0.1.1

- **add** `txt delete` 删除时有 y/n 确认。

### v0.1.0

- **add** `txt send -g/--gui` 打开 GUI 窗口发送消息，可方便地避免字符转义问题。

### v0.0.9

- **add** `txt getkey -forget` 清除密钥，相当于登出，需要重新获取密钥才能正常使用

### v0.0.8

- **add** `txt send` 默认发送系统剪贴板的内容，好处是方便，而且不用担心字符转义的问题。
- **change** `txt send Hello World!` 多数情况下不需要加双引号把句子包裹起来。但要注意字符转义的问题。例如 `txt send He said: "Hello World!"` 会被转义成 `He said: Hello World!` (半角双引号不见了)。
- **add** 对于遇到字符转义问题，并且无法读取系统剪贴板的情况，还可以用 `txt send -f ./file.txt` 的方式发送文件内容。
