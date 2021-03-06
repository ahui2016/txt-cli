import json
import arrow
import pyperclip
import requests
from pathlib import Path
from typing import cast
from appdirs import AppDirs
from urllib.parse import urljoin
from txtcli.model import Alias, ErrMsg, SecretKey, TxtConfig, TxtMsg

DateFormat = "YYYY-MM-DD"
cfg_file_name = "txt-config.json"

temp_bucket = "temporary-bucket"
perm_bucket = "permanent-bucket"

app_dirs = AppDirs("txt-cli", "github-ahui2016")
app_config_dir = Path(app_dirs.user_config_dir)
cfg_path = app_config_dir.joinpath(cfg_file_name)


def postTimeout(url: str, data: dict) -> requests.Response:
    return requests.post(url, data=data, timeout=5)


def init_cfg() -> None:
    app_config_dir.mkdir(parents=True, exist_ok=True)
    if not cfg_path.exists():
        with open(cfg_path, "w", encoding="utf-8") as f:
            cfg = TxtConfig(
                server="https://txt-demo.ai42.cc",
                secret_key="",
                txt_default=5,
                txt_list_default=9,
            )
            json.dump(cfg, f, indent=4, ensure_ascii=False)


def load_cfg() -> TxtConfig:
    with open(cfg_path, "rb") as f:
        return cast(TxtConfig, json.load(f))


def update_cfg(cfg: TxtConfig) -> None:
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)


def forget_key() -> None:
    cfg = load_cfg()
    cfg["secret_key"] = ""
    update_cfg(cfg)
    print("OK. 已清除密钥。")


def get_key(pwd: str) -> ErrMsg:
    cfg = load_cfg()
    url = urljoin(cfg["server"], "/auth/get-current-key")
    r = postTimeout(url, data={"password": pwd})
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    key = cast(SecretKey, r.json())
    if cfg["secret_key"] != key["Key"]:
        cfg["secret_key"] = key["Key"]
        update_cfg(cfg)

    keyStarts = arrow.get(key["Starts"]).format(DateFormat)
    keyExpires = arrow.get(key["Expires"]).format(DateFormat)
    status = "有效" if key["IsGood"] else "已过期"
    print(f"获取密钥成功, 有效期 {keyStarts} 至 {keyExpires}, 状态:{status}")
    return None


def gen_new_key(pwd: str) -> ErrMsg:
    cfg = load_cfg()
    url = urljoin(cfg["server"], "/auth/gen-new-key")
    r = postTimeout(url, data={"password": pwd})
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    key = cast(SecretKey, r.json())
    cfg["secret_key"] = key["Key"]
    update_cfg(cfg)
    keyStarts = arrow.get(key["Starts"]).format(DateFormat)
    keyExpires = arrow.get(key["Expires"]).format(DateFormat)
    print(f"生成新密钥, 有效期 {keyStarts} 至 {keyExpires} (注意，旧密钥已失效)")
    return None


def printTxtMsg(msg: TxtMsg) -> None:
    item_title = f'[{msg["Cat"][0]}{msg["Index"]}] [{msg["ID"]}]'
    if msg["Alias"]:
        item_title += f' [{msg["Alias"]}]'

    print(item_title)
    print(msg["Msg"])
    print()


def get_txt(cfg:TxtConfig,bucket: str = "", index: int = 1, limit: int = 0) -> ErrMsg:
    if index <= 1:
        index = 1
    if limit <= 0:
        if bucket:
            limit = cfg["txt_list_default"]
        else:
            limit = cfg["txt_default"]
    if bucket != perm_bucket:
        bucket = temp_bucket

    r = postTimeout(
        urljoin(cfg["server"], "/cli/get-more-items"),
        data=dict(bucket=bucket, index=index, limit=limit, password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    items = cast(list[TxtMsg], r.json())
    if items is None or len(items) == 0:
        return "Not Found (找不到指定消息)"

    for item in items:
        printTxtMsg(item)

    return None


def get_one(cfg: TxtConfig, a_or_i: str, copy: bool = True) -> ErrMsg:
    r = postTimeout(
        urljoin(cfg["server"], "/cli/get-by-a-or-i"),
        data=dict(a_or_i=a_or_i, password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    item = cast(TxtMsg, r.json())
    if copy:
        try:
            pyperclip.copy(item["Msg"])
        except Exception:
            pass
        print(item["Msg"])
    else:
        printTxtMsg(item)
    return None


def get_aliases(cfg:TxtConfig) -> ErrMsg:
    r = postTimeout(
        urljoin(cfg["server"], "/cli/get-all-aliases"),
        data=dict(password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    all = cast(list[Alias], r.json())
    aliases = [a["ID"] for a in all]
    print(", ".join(aliases))
    return None


def send_msg(msg: str) -> ErrMsg:
    cfg = load_cfg()
    r = postTimeout(
        urljoin(cfg["server"], "/cli/add"),
        data=dict(msg=msg, password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    return get_txt(cfg, limit=1)


def toggle_cat(a_or_i: str) -> ErrMsg:
    cfg = load_cfg()
    r = postTimeout(
        urljoin(cfg["server"], "/cli/toggle-category"),
        data=dict(a_or_i=a_or_i, password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    print("OK. Indexes are changed. (注意，流水号已发生变化)")
    return None


def delete_msg(cfg: TxtConfig, a_or_i: str) -> ErrMsg:
    r = postTimeout(
        urljoin(cfg["server"], "/cli/delete"),
        data=dict(a_or_i=a_or_i, password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    print("Deleted, and indexes are updated. (已删除，并且流水号已发生变化)")
    return None


def set_alias(cfg: TxtConfig, a_or_i: str, alias: str) -> ErrMsg:
    r = postTimeout(
        urljoin(cfg["server"], "/cli/set-alias"),
        data=dict(a_or_i=a_or_i, alias=alias, password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    if alias:
        err = get_one(cfg, alias, copy=False)
    else:
        err = get_one(cfg, a_or_i, copy=False)
    return err


def search_msg(keyword: str) -> ErrMsg:
    cfg = load_cfg()
    r = postTimeout(
        urljoin(cfg["server"], "/cli/search"),
        data=dict(keyword=keyword, password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    items = cast(list[TxtMsg], r.json())
    if items is None or len(items) == 0:
        return "Not Found (找不到相关消息)"

    items.sort(key=lambda x: x["ID"], reverse=True)
    for item in items:
        printTxtMsg(item)

    return None
