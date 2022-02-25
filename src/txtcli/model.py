from typing import TypedDict


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
