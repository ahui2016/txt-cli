# txt-cli

The CLI tool for ahui2016/txt


## Features (功能)

- `txt` 列出最近 5 条消息
- `txt next` 列出后续 5 条消息（暂时不做这个功能）
- `txt get [index/alias]` 通过 index 或别名获取(复制，同时打印到屏幕)一条消息，默认获取 T1
- `txt send [message]` 发送消息 (添加暂存消息)
- `txt list [n]` 列出最近 n 条消息 (包括暂存消息与永久消息，默认 n = 9)
- `txt list -t [n]` 列出最近 n 条暂存消息（默认 n = 9）
- `txt list -p [n]` 列出最近 n 条永久消息（默认 n = 9）
- `txt list [n] -from [when]` 列出从 when 开始的 n 条消息
- `txt toggle [index]` 切换一条消息的状态(暂存/永久), 默认把 T1 切换为 P1
- `txt alias [index] [alias]` 为一条消息设置别名
- `txt search [keyword]` 搜索消息


其中，`index` 是消息的索引，每当添加消息、删除消息、转换状态时都会导致索引发生变化，以 T 开头的索引表示暂存消息，以 P 开头表示永久消息，比如 `T1` 表示最新一条暂存消息, `P3` 表示第 3 条永久消息，其中 T/P 不分大小写。

`alias` 是消息的别名，一个别名只能对应一条消息。不可采用“以 T 或 P 开头紧跟数字”的形式（要避免与 index 冲突）。

`when` 是消息的 ID, 同时也是消息的创建时间，可以只使用 ID 的开头一部分，例如 `txt list 10 -from '2022-02-24'`
