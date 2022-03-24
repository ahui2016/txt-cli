import click
import pyperclip
from txtcli.gui import tk_send_msg
from txtcli.model import ErrMsg

from txtcli.util import (
    cfg_path,
    delete_msg,
    forget_key,
    gen_new_key,
    get_aliases,
    get_one,
    search_msg,
    send_msg,
    set_alias,
    temp_bucket,
    perm_bucket,
    get_key,
    get_txt,
    init_cfg,
    load_cfg,
    toggle_cat,
    update_cfg,
)

from . import (
    __version__,
    __package_name__,
)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def check(ctx: click.Context, errMsg: ErrMsg) -> None:
    """检查 err, 有错误则打印并终止程序，无错误则什么都不用做。"""
    if errMsg:
        click.echo(f"Error: {errMsg}", err=True)
        ctx.exit()


def invalid_index(ctx: click.Context, index: str):
    click.echo(f"'{index}' is not a valid index. (格式错误)")
    click.echo("Try 'txt list -h' for help.")
    ctx.exit()


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
    "-V",
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
        check(ctx, get_txt(cfg))
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
@click.option("gen", "-gen", "--generate", is_flag=True, help="generate a new key")
@click.option("forget", "-forget", "--forget-key", is_flag=True, help="forget the key")
@click.pass_context
def getkey(ctx: click.Context, gen: bool, forget: bool):
    """Get the current secret key, or generate a new key.

    获取日常操作密钥，或生成新的密钥。注意，一旦生成新密钥，旧密钥就失效。
    """
    if forget:
        forget_key()
        ctx.exit()

    pwd = click.prompt("master password", hide_input=True)
    if gen:
        errMsg = gen_new_key(pwd)
    else:
        errMsg = get_key(pwd)

    check(ctx, errMsg)
    ctx.exit()


@cli.command(context_settings=CONTEXT_SETTINGS, name="list")
@click.option("n", "-n", type=int, default=0, help="how many items to show")
@click.option("alias", "-a", "--alias", is_flag=True, help="show all aliases")
@click.argument("index", default="t1")
@click.pass_context
def list_command(ctx: click.Context, alias: bool, index: str, n: int):
    """List out messages or aliases.

    [INDEX] 的格式是 't1', 't2', 'p1', 'p2'... 依此类推。缺省值是 't1'。

    Example 1: txt list (列出最近几条暂存消息)

    Example 2: txt list p1 (列出最近几条永久消息)

    Example 3: txt list p3 -n 5 (从第 3 条永久消息开始，列出 5 条永久消息)

    Example 4: txt list --alias (列出全部别名)
    """
    cfg = load_cfg()

    if alias:
        check(ctx, get_aliases(cfg))
        ctx.exit()

    if len(index) < 2:
        invalid_index(ctx, index)

    if index[0].upper() == "P":
        bucket = perm_bucket
    elif index[0].upper() == "T":
        bucket = temp_bucket
    else:
        invalid_index(ctx, index)

    try:
        i = int(index[1:])
    except ValueError:
        invalid_index(ctx, index)

    check(ctx, get_txt(cfg, bucket, i, n))
    ctx.exit()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("a_or_i", nargs=1, default="t1")
@click.pass_context
def get(ctx: click.Context, a_or_i: str):
    """Get a message by alias or index.

    通过别名或流水号获取一条消息 (打印到屏幕并复制到剪贴板), 默认获取 't1'。

    [A_OR_I] 既可以是别名，也可以是流水号。

    Example 1: txt get

    Example 2: txt get p1

    Example 3: txt get my-email
    """
    cfg = load_cfg()
    check(ctx, get_one(cfg, a_or_i))
    ctx.exit()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "gui", "-g", "--gui", is_flag=True, help="Open a GUI window for text input."
)
@click.option(
    "filename",
    "-f",
    "--file",
    type=click.Path(exists=True),
    help="Send the content of the file.",
)
@click.argument("msg", nargs=-1)
@click.pass_context
def send(ctx: click.Context, gui: bool, msg: str, filename: str):
    """Send a message. (发送一条消息)

    Example 1: txt send  (默认发送系统剪贴板的内容)

    Example 2: txt send Hello world! (发送 'Hello world!')

    Example 3: txt send -f ./file.txt (发送文件内容)
    """
    if gui:
        try:
            check(ctx, tk_send_msg())
        except Exception:
            pass
        ctx.exit()

    if filename:
        with open(filename, "r", encoding="utf-8") as f:
            msg = f.read()
        check(ctx, send_msg(msg))
        ctx.exit()

    if msg:
        msg = " ".join(msg).strip()
    else:
        try:
            msg = pyperclip.paste()
        except Exception:
            pass

    check(ctx, send_msg(msg))
    ctx.exit()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("a_or_i", nargs=1, default="t1")
@click.pass_context
def toggle(ctx: click.Context, a_or_i: str):
    """Toggle the category of a message.

    切换一条消息的类型 (暂存/永久), 默认把 T1 切换为 P1。

    [A_OR_I] 既可以是别名，也可以是流水号。

    Example 1: txt toggle (把 t1 切换为永久消息)

    Example 2: txt toggle p1 (把 p1 切换为暂存消息)

    Example 3: txt toggle my-email (切换别名为 my-email 的类型)
    """
    check(ctx, toggle_cat(a_or_i))
    ctx.exit()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("a_or_i", nargs=1, required=True)
@click.pass_context
def delete(ctx: click.Context, a_or_i: str):
    """Delete a message. (删除一条消息)

    [A_OR_I] 既可以是别名，也可以是流水号。

    Example 1: txt delete t2 (删除t2)

    Example 2: txt delete p1 (删除p1)

    Example 3: txt delete my-email (删除别名为 my-email 的消息)
    """
    cfg = load_cfg()
    check(ctx, get_one(cfg, a_or_i, False))
    click.confirm("Confirm deletion (确认删除，不可恢复)", abort=True)
    check(ctx, delete_msg(cfg, a_or_i))
    ctx.exit()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option("delete", "--delete", is_flag=True, help="delete the alias")
@click.argument("args", nargs=-1, required=True)
@click.pass_context
def alias(ctx: click.Context, delete: bool, args: tuple):
    """Set or delete the alias of a message.

    设置或删除别名。

    [ARGS] 是两个字符串，第一个是流水号或旧别名，第二个是新别名。

    Example 1: txt alias t1 my-email (把 't1' 的别名设为 'my-email')

    Example 2: txt alias my-email email (把别名 'my-email' 改为 'email')

    Example 3: txt alias --delete email (删除别名 'email')
    """
    if delete:
        if args and len(args) != 1:
            click.echo("Error: Argument 'args' takes 1 value when use with '--delete'.")
            ctx.exit()
        args = (args[0], "")

    if len(args) != 2:
        click.echo("Error: Argument 'args' takes 2 values.")
        ctx.exit()

    cfg = load_cfg()
    check(ctx, set_alias(cfg, args[0], args[1]))
    ctx.exit()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("keyword", nargs=1, required=True)
@click.pass_context
def search(ctx: click.Context, keyword: str):
    """Search messages by a keyword. (查找消息)

    Example: txt search hello (查找包含 'hello' 的消息)
    """
    check(ctx, search_msg(keyword))
    ctx.exit()


# 初始化
init_cfg()

if __name__ == "__main__":
    cli(obj={})
