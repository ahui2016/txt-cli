# txt-cli

The CLI tool for ahui2016/txt


## Features (功能)

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

- `txt getkey` 获取密钥（同时提示密钥状态），需要输入主密码
- `txt getkey -gen/--generate` 生产新密钥，需要输入主密码
- `txt changepwd` 更改主密码 (暂时不做这个功能)
- `txt server` 查看当前服务器地址
- `txt server -set [url]` 修改服务器地址


其中，`index` 是消息的流水号，每当添加消息、删除消息、转换状态时都会导致流水号发生变化，以 T 开头的流水号表示暂存消息，以 P 开头表示永久消息，比如 `T1` 表示最新一条暂存消息, `P3` 表示第 3 条永久消息，其中 T/P 不分大小写。

`alias` 是消息的别名，一个别名只能对应一条消息。不可采用“以 T 或 P 开头紧跟数字”的形式（要避免与 index 冲突）。

