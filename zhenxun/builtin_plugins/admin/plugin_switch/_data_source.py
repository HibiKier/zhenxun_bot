from zhenxun.models.group_console import GroupConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.task_info import TaskInfo
from zhenxun.utils.enum import BlockType, PluginType
from zhenxun.utils.exception import GroupInfoNotFound
from zhenxun.utils.image_utils import BuildImage, ImageTemplate, RowStyle


def plugin_row_style(column: str, text: str) -> RowStyle:
    """被动技能文本风格

    参数:
        column: 表头
        text: 文本内容

    返回:
        RowStyle: RowStyle
    """
    style = RowStyle()
    if column == "全局状态":
        if text == "开启":
            style.font_color = "#67C23A"
        else:
            style.font_color = "#F56C6C"
    if column == "加载状态":
        if text == "SUCCESS":
            style.font_color = "#67C23A"
        else:
            style.font_color = "#F56C6C"
    return style


async def build_plugin() -> BuildImage:
    column_name = [
        "ID",
        "模块",
        "名称",
        "全局状态",
        "禁用类型",
        "加载状态",
        "菜单分类",
        "作者",
        "版本",
        "金币花费",
    ]
    plugin_list = await PluginInfo.filter(plugin_type__not=PluginType.HIDDEN).all()
    column_data = []
    for plugin in plugin_list:
        column_data.append(
            [
                plugin.id,
                plugin.module,
                plugin.name,
                "开启" if plugin.status else "关闭",
                plugin.block_type,
                "SUCCESS" if plugin.load_status else "ERROR",
                plugin.menu_type,
                plugin.author,
                plugin.version,
                plugin.cost_gold,
            ]
        )
    return await ImageTemplate.table_page(
        "Plugin",
        "插件状态",
        column_name,
        column_data,
        text_style=plugin_row_style,
    )


def task_row_style(column: str, text: str) -> RowStyle:
    """被动技能文本风格

    参数:
        column: 表头
        text: 文本内容

    返回:
        RowStyle: RowStyle
    """
    style = RowStyle()
    if column in ["群组状态", "全局状态"]:
        if text == "开启":
            style.font_color = "#67C23A"
        else:
            style.font_color = "#F56C6C"
    return style


async def build_task(group_id: str | None) -> BuildImage:
    """构造被动技能状态图片

    参数:
        group_id: 群组id

    异常:
        GroupInfoNotFound: 未找到群组

    返回:
        BuildImage: 被动技能状态图片
    """
    task_list = await TaskInfo.all()
    column_name = ["ID", "模块", "名称", "群组状态", "全局状态", "运行时间"]
    group = None
    if group_id:
        group = await GroupConsole.get_or_none(group_id=group_id)
        if not group:
            raise GroupInfoNotFound()
    else:
        column_name.remove("群组状态")
    column_data = []
    for task in task_list:
        if group:
            column_data.append(
                [
                    task.id,
                    task.module,
                    task.name,
                    "开启" if task.module not in group.block_task else "关闭",
                    "开启" if task.status else "关闭",
                    task.run_time,
                ]
            )
        else:
            column_data.append(
                [
                    task.id,
                    task.module,
                    task.name,
                    "开启" if task.status else "关闭",
                    task.run_time,
                ]
            )
    return await ImageTemplate.table_page(
        "Task",
        "被动技能状态",
        column_name,
        column_data,
        text_style=task_row_style,
    )


class PluginManage:

    @classmethod
    async def block(cls, module: str):
        await PluginInfo.filter(module=module).update(status=False)

    @classmethod
    async def unblock(cls, module: str):
        await PluginInfo.filter(module=module).update(status=True)

    @classmethod
    async def block_group_plugin(cls, plugin_name: str, group_id: str) -> str:
        """禁用群组插件

        参数:
            plugin_name: 插件名称
            group_id: 群组id

        返回:
            str: 返回信息
        """
        return await cls._change_group_plugin(plugin_name, group_id, True)

    @classmethod
    async def unblock_group_plugin(cls, plugin_name: str, group_id: str) -> str:
        """启用群组插件

        参数:
            plugin_name: 插件名称
            group_id: 群组id

        返回:
            str: 返回信息
        """
        return await cls._change_group_plugin(plugin_name, group_id, False)

    @classmethod
    async def _change_group_plugin(
        cls, plugin_name: str, group_id: str, status: bool
    ) -> str:
        """修改群组插件状态

        参数:
            plugin_name: 插件名称
            group_id: 群组id
            status: 插件状态

        返回:
            str: 返回信息
        """
        status_str = "开启" if status else "关闭"
        if plugin := await PluginInfo.get_or_none(name=plugin_name):
            group, _ = await GroupConsole.get_or_create(group_id=group_id)
            if status:
                if plugin.module in group.block_plugin:
                    group.block_plugin = group.block_plugin.replace(
                        f"{plugin.module},", ""
                    )
                    await group.save(update_fields=["block_plugin"])
                    return f"已成功{status_str} {plugin_name} 功能!"
            else:
                if plugin.module not in group.block_plugin:
                    group.block_plugin += f"{plugin.module},"
                    await group.save(update_fields=["block_plugin"])
                    return f"已成功{status_str} {plugin_name} 功能!"
            return f"该功能已经{status_str}了喔，不要重复{status_str}..."
        return "没有找到这个功能喔..."

    @classmethod
    async def superuser_block(
        cls, plugin_name: str, block_type: BlockType | None, group_id: str | None
    ) -> str:
        """超级用户禁用

        参数:
            plugin_name: 插件名称
            block_type: 禁用类型
            group_id: 群组id

        返回:
            str: 返回信息
        """
        if plugin := await PluginInfo.get_or_none(name=plugin_name):
            if group_id:
                if group := await GroupConsole.get_or_none(group_id=group_id):
                    if f"super:{plugin_name}," not in group.block_plugin:
                        group.block_plugin += f"super:{plugin_name},"
                        await group.save(update_fields=["block_plugin"])
                        return (
                            f"已成功关闭群组 {group.group_name} 的 {plugin_name} 功能!"
                        )
                    return "此群组该功能已被超级用户关闭，不要重复关闭..."
                return "群组信息未更新，请先更新群组信息..."
            plugin.block_type = block_type
            plugin.status = not bool(block_type)
            await plugin.save(update_fields=["status", "block_type"])
            if not block_type:
                return f"已成功将 {plugin_name} 全局启用!"
            else:
                return f"已成功将 {plugin_name} 全局关闭!"
        return "没有找到这个功能喔..."
