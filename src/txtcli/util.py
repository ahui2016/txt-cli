import json
from pathlib import Path
from appdirs import AppDirs

from txtcli.model import TxtConfig

cfg_file_name = "txt-config.json"

app_dirs = AppDirs("txt-cli", "github-ahui2016")
app_config_dir = Path(app_dirs.user_config_dir)
cfg_path = app_config_dir.joinpath(cfg_file_name)


def ensure_cfg_file() -> None:
    app_config_dir.mkdir(parents=True, exist_ok=True)
    if not cfg_path.exists():
        with open(cfg_path, "w", encoding="utf-8") as f:
            cfg = TxtConfig(
                server="https://txt-demo.ai42.xyz",
                secret_key="",
                txt_default=5,
                txt_list_default=10,)
            json.dump(cfg, f, indent=4, ensure_ascii=False)
