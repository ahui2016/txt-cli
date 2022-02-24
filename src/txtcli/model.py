from typing import TypedDict


class TxtConfig(TypedDict):
    server: str
    secret_key: str
    txt_default: int # 命令 `txt`` 列出消息条数的默认值
    txt_list_default: int # 命令 `txt list`` 列出消息条数的默认值
