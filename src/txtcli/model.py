from typing import TypedDict


# 采用 ErrMsg 而不是采用 exception, 一来是受到 Go 语言的影响，
# 另一方面，凡是用到 ErrMsg 的地方都是与业务逻辑密切相关并且需要向用户反馈详细错误信息的地方，
# 这些地方用 ErrMsg 更合理。 (以后会改用 pypi.org/project/result)
ErrMsg = str | None
"""一个描述错误内容的简单字符串, None 表示无错误。"""


class TxtConfig(TypedDict):
    server: str  # 服务器地址，例如 https://txt-demo.ai42.xyz
    secret_key: str
    txt_default: int  # 命令 `txt` 的 n 参数的默认值
    txt_list_default: int  # 命令 `txt list` 的 n 参数的默认值


class SecretKey(TypedDict):
    Key: str
    Starts: int
    MaxAge: int
    Expires: int
    IsGood: bool
