import click

from txtcli.util import get_key, init_cfg, load_cfg, update_cfg

from . import (
    __version__,
    __package_name__,
)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(invoke_without_command=True)
@click.help_option("-h", "--help")
@click.version_option(
    __version__,
    "-V",
    "--version",
    package_name=__package_name__,
    message="%(prog)s version: %(version)s",
)
@click.pass_context
def cli(ctx: click.Context):
    """txt-cli: The CLI tool for ahui2016/txt

    https://pypi.org/project/txtcli/
    """
    pass


# 以上是主命令
############
# 以下是子命令


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option("server_url", "-set", help="set the server url")
@click.pass_context
def server(ctx: click.Context, server_url:str):
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
