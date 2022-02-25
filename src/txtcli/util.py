import json
import arrow
import requests
from pathlib import Path
from typing import cast
from appdirs import AppDirs
from urllib.parse import urljoin
from txtcli.model import SecretKey, TxtConfig

DateFormat = "YYYY-MM-DD"
cfg_file_name = "txt-config.json"

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
                txt_list_default=10,
            )
            json.dump(cfg, f, indent=4, ensure_ascii=False)


def load_cfg() -> TxtConfig:
    with open(cfg_path, "rb") as f:
        return cast(TxtConfig, json.load(f))


def update_cfg(cfg: TxtConfig) -> None:
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)


def get_key(pwd: str) -> None:
    cfg = load_cfg()
    url = urljoin(cfg["server"], "/auth/get-current-key")
    r = requests.post(url, data={"password": pwd})
    if r.status_code != 200:
        raise Exception(f"{r.status_code}: {r.text}")
    key = cast(SecretKey, r.json())
    cfg["secret_key"] = key["Key"]
    update_cfg(cfg)
    keyStarts = arrow.get(key["Starts"]).format(DateFormat)
    keyExpires = arrow.get(key["Expires"]).format(DateFormat)
    status = "有效" if key["IsGood"] else "已过期"
    print(f"获取密钥成功, 有效期 {keyStarts} 至 {keyExpires}, 状态: {status}")
