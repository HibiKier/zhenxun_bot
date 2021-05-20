from nonebot.rule import ArgumentParser

from .handle import *

npm_parser = ArgumentParser("npm", add_help=False)
npm_parser.add_argument(
    "-h", "--help", action="store_true", help="show this help message and exit"
)

npm_subparsers = npm_parser.add_subparsers()

list_parser = npm_subparsers.add_parser("list", help="show plugin list")
list_parser.add_argument(
    "-s", "--store", action="store_true", help="show plugin store list"
)
list_parser.add_argument(
    "-d", "--default", action="store_true", help="show default plugin list"
)
list_parser.add_argument("-g", "--group", action="store", help="show group plugin list")
list_parser.set_defaults(handle=handle_list)

block_parser = npm_subparsers.add_parser("block", help="block plugin")
block_parser.add_argument("plugins", nargs="*", help="plugins you want to block")
block_parser.add_argument("-d", "--default", action="store_true", help="set default")
block_parser.add_argument("-a", "--all", action="store_true", help="select all plugin")
block_parser.add_argument("-g", "--group", action="store", help="set in group")
block_parser.set_defaults(handle=handle_block)

unblock_parser = npm_subparsers.add_parser("unblock", help="unblock plugin")
unblock_parser.add_argument("plugins", nargs="*", help="plugins you want to unblock")
unblock_parser.add_argument("-d", "--default", action="store_true", help="set default")
unblock_parser.add_argument(
    "-a", "--all", action="store_true", help="select all plugin"
)
unblock_parser.add_argument("-g", "--group", action="store", help="set in group")
unblock_parser.set_defaults(handle=handle_unblock)

info_parser = npm_subparsers.add_parser("info", help="show plugin info")
info_parser.add_argument("plugin", help="plugins you want to know")
info_parser.set_defaults(handle=handle_info)

install_parser = npm_subparsers.add_parser("install", help="install plugin")
install_parser.add_argument("plugins", nargs="*", help="plugins you want to install")
install_parser.add_argument("-i", "--index", action="store", help="point to a mirror")
install_parser.set_defaults(handle=handle_install)

update_parser = npm_subparsers.add_parser("update", help="update plugin")
update_parser.add_argument("plugins", nargs="*", help="plugins you want to update")
update_parser.add_argument("-a", "--all", action="store_true", help="select all plugin")
update_parser.add_argument("-i", "--index", action="store", help="point to a mirror")
update_parser.set_defaults(handle=handle_update)

uninstall_parser = npm_subparsers.add_parser("uninstall", help="uninstall plugin")
uninstall_parser.add_argument(
    "plugins", nargs="*", help="plugins you want to uninstall"
)
uninstall_parser.add_argument(
    "-a", "--all", action="store_true", help="select all plugin"
)
uninstall_parser.set_defaults(handle=handle_uninstall)
