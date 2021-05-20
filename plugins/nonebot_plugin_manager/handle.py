from argparse import Namespace

from .data import *


def handle_list(
    args: Namespace,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    message = ""

    if args.store:
        if is_superuser:
            return get_store_pulgin_list()
        else:
            return "获取商店插件列表需要超级用户权限！"

    if args.default:
        if is_superuser:
            group_id = "default"
            message += "默认"
        else:
            return "获取默认插件列表需要超级用户权限！"

    if args.group:
        if is_superuser:
            group_id = args.group
            message += f"群{args.group}"
        else:
            return "获取指定群插件列表需要超级用户权限！"

    message += "插件列表如下：\n"
    message += "\n".join(
        f"[{'o' if get_group_plugin_list(group_id)[plugin] else 'x'}] {plugin}"
        for plugin in get_group_plugin_list(group_id)
    )
    return message


def handle_block(
    args: Namespace,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:

    if not is_admin and not is_superuser:
        return "管理插件需要群管理员权限！"

    message = ""

    if args.default:
        if is_superuser:
            group_id = "default"
            message += "默认"
        else:
            return "管理默认插件需要超级用户权限！"

    if args.group:
        if is_superuser:
            group_id = args.group
            message += f"群{args.group}"
        else:
            return "管理指定群插件需要超级用户权限！"

    message += block_plugin(group_id, *args.plugins)
    return message


def handle_unblock(
    args: Namespace,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    message = ""

    if not is_admin and not is_superuser:
        return "管理插件需要群管理员权限！"

    if args.default:
        if is_superuser:
            group_id = "default"
            message += "默认"
        else:
            return "管理默认插件需要超级用户权限！"

    if args.group:
        if is_superuser:
            group_id = args.group
            message += f"群{args.group}"
        else:
            return "管理指定群插件需要超级用户权限！"

    message += unblock_plugin(group_id, *args.plugins)
    return message


def handle_info(
    args: Namespace,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:

    if not is_admin and not is_superuser:
        return "管理插件需要超级权限！"

    return get_store_plugin_info(args.plugin)


def handle_install(
    args: Namespace,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    pass


def handle_update(
    args: Namespace,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    pass


def handle_uninstall(
    args: Namespace,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    pass
