import click

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
def cli(ctx):
    """txt-cli: The CLI tool for ahui2016/txt

    https://pypi.org/project/txtcli/
    """
    pass


# 以上是主命令
############
# 以下是子命令
