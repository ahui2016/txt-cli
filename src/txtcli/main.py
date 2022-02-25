import click

from txtcli.util import (
    cfg_path,
    temp_bucket,
    perm_bucket,
    get_key,
    get_txt,
    init_cfg,
    load_cfg,
    update_cfg,
)

from . import (
    __version__,
    __package_name__,
)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def show_where(ctx: click.Context, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"[txt] {__file__}")
    click.echo(f"[config] {cfg_path}")
    ctx.exit()


@click.group(invoke_without_command=True)
@click.help_option("-h", "--help")
@click.version_option(
    __version__,
    "-v",
    "--version",
    package_name=__package_name__,
    message="%(prog)s version: %(version)s",
)
@click.option(
    "-w",
    "--where",
    is_flag=True,
    help="Show locations about txt-cli.",
    expose_value=False,
    callback=show_where,
)
@click.pass_context
def cli(ctx: click.Context):
    """txt-cli: The CLI tool for ahui2016/txt

    https://pypi.org/project/txtcli/
    """
    if ctx.invoked_subcommand is None:
        cfg = load_cfg()
        err = get_txt(cfg)
        if err:
            click.echo(err)
        ctx.exit()


# 以上是主命令
############
# 以下是子命令


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option("server_url", "-set", help="set the server url")
@click.pass_context
def server(ctx: click.Context, server_url: str):
    """Show or set the server url. (获取或设置服务器地址)"""
    cfg = load_cfg()
    if not server_url:
        click.echo(cfg["server"])
    else:
        cfg["server"] = server_url
        update_cfg(cfg)
        click.echo("OK.")
    ctx.exit()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def getkey(ctx: click.Context):
    """Get the secret key. (获取日常操作密钥)"""
    pwd = click.prompt("master password", hide_input=True)
    err = get_key(pwd)
    if err:
        click.echo(err)
    ctx.exit()


# 初始化
init_cfg()

if __name__ == "__main__":
    cli(obj={})
