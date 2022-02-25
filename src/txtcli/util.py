import json
import arrow
import requests
from pathlib import Path
from typing import cast
from appdirs import AppDirs
from urllib.parse import urljoin
from txtcli.model import ErrMsg, SecretKey, TxtConfig, TxtMsg

DateFormat = "YYYY-MM-DD"
cfg_file_name = "txt-config.json"

temp_bucket = "temporary-bucket"
perm_bucket = "permanent-bucket"

app_dirs = AppDirs("txt-cli", "github-ahui2016")
app_config_dir = Path(app_dirs.user_config_dir)
cfg_path = app_config_dir.joinpath(cfg_file_name)


def init_cfg() -> None:
    app_config_dir.mkdir(parents=True, exist_ok=True)
    if not cfg_path.exists():
        with open(cfg_path, "w", encoding="utf-8") as f:
            cfg = TxtConfig(
                server="https://txt-demo.ai42.xyz",
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


def get_key(pwd: str) -> ErrMsg:
    cfg = load_cfg()
    url = urljoin(cfg["server"], "/auth/get-current-key")
    r = requests.post(url, data={"password": pwd})
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


def get_txt(
    bucket: str = temp_bucket, index: int = 1, limit: int = 0
) -> ErrMsg:
    cfg = load_cfg()
    if index <= 1:
        index = 1
    if limit <= 0:
        limit = cfg["txt_default"]
    if bucket != perm_bucket:
        bucket = temp_bucket

    r = requests.post(
        urljoin(cfg["server"], "/cli/get-more-items"),
        data=dict(bucket=bucket, index=index, limit=limit, password=cfg["secret_key"]),
    )
    if r.status_code != 200:
        return f"{r.status_code}: {r.text}"

    items = cast(list[TxtMsg], r.json())
    for item in items:
        item_index = f'{item["Cat"][0]}{item["Index"]}'
        if item["Alias"]:
            msg = f"[{item['Alias']}] {item['Msg']}"
        else:
            msg = item["Msg"]

        print(f"[{item_index}] [{item['ID']}]")
        print(msg)
        print()

    return None
