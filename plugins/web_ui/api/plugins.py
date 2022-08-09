from pydantic import ValidationError

from configs.config import Config
from services.log import logger
from utils.manager import (plugins2block_manager, plugins2cd_manager,
                           plugins2count_manager, plugins2settings_manager,
                           plugins_manager)
from utils.utils import get_matchers

from ..auth import Depends, User, token_to_user
from ..config import *

plugin_name_list = None


@app.get("/webui/plugins")
def _(type_: Optional[str], user: User = Depends(token_to_user)) -> Result:
    """
    获取插件列表
    :param type_: 类型 normal, superuser, hidden, admin
    """
    global plugin_name_list
    if not plugin_name_list:
        plugin_name_list = [x.plugin_name for x in get_matchers()]
    plugin_list = []
    plugin_data = plugins_manager.get_data()
    for model in plugin_data:
        if model in plugin_name_list:
            try:
                data = plugin_data.get(model)
                data["model"] = model
                plugin_name = data.get("plugin_name")
                if (
                    (type_ == "hidden" and "[hidden]" not in plugin_name.lower())
                    or (type_ == "admin" and "[admin]" not in plugin_name.lower())
                    or (
                        type_ == "superuser"
                        and "[superuser]" not in plugin_name.lower()
                    )
                ):
                    continue
                if type_ == "normal" and (
                    "[hidden]" in plugin_name.lower()
                    or "[admin]" in plugin_name.lower()
                    or "[superuser]" in plugin_name.lower()
                ):
                    continue
                data = {"model": model}
                if x := plugin_data.get(model):
                    if not x.get("status") and x.get("block_type") in [
                        "group",
                        "private",
                        "all",
                    ]:
                        x["block_type"] = (
                            "群聊"
                            if x["block_type"] == "group"
                            else "私聊"
                            if x["block_type"] == "private"
                            else "全部"
                        )
                    data["plugin_manager"] = PluginManager(**x)
                if x := plugins2settings_manager.get(model):
                    if x.get("cmd") and isinstance(x.get("cmd"), list):
                        x["cmd"] = ",".join(x["cmd"])
                    data["plugin_settings"] = PluginSettings(**x)
                if x := plugins2cd_manager.get(model):
                    data["cd_limit"] = CdLimit(**x)
                if x := plugins2block_manager.get(model):
                    data["block_limit"] = BlockLimit(**x)
                if x := plugins2count_manager.get(model):
                    data["count_limit"] = CountLimit(**x)
                if x := Config.get(model):
                    id_ = 0
                    tmp = []
                    for key in x.keys():
                        tmp.append(
                            PluginConfig(
                                **{
                                    "key": key,
                                    "help_": x[key].get("help"),
                                    "id": id_,
                                    **x[key],
                                }
                            )
                        )
                        id_ += 1
                    data["plugin_config"] = tmp
                plugin_list.append(Plugin(**data))
            except (AttributeError, ValidationError) as e:
                logger.error(
                    f"WEB_UI GET /webui/plugins model：{model} 发生错误 {type(e)}：{e}"
                )
            except Exception as e:
                logger.error(
                    f"WEB_UI GET /webui/plugins model：{model} 发生错误 {type(e)}：{e}"
                )
                return Result(
                    code=500,
                    data=f"WEB_UI GET /webui/plugins model：{model} 发生错误 {type(e)}：{e}",
                )
    return Result(code=200, data=plugin_list)


@app.post("/webui/plugins")
def _(plugin: Plugin, user: User = Depends(token_to_user)) -> Result:
    """
    修改插件信息
    :param plugin: 插件内容
    """
    try:
        if plugin.plugin_config:
            for c in plugin.plugin_config:
                if not c.value:
                    Config.set_config(plugin.model, c.key, None)
                    continue
                if str(c.value).lower() in ["true", "false"] and (
                    c.default_value is None or isinstance(c.default_value, bool)
                ):
                    c.value = str(c.value).lower() == "true"
                elif isinstance(
                    Config.get_config(plugin.model, c.key, c.value), int
                ) or isinstance(c.default_value, int):
                    c.value = int(c.value)
                elif isinstance(
                    Config.get_config(plugin.model, c.key, c.value), float
                ) or isinstance(c.default_value, float):
                    c.value = float(c.value)
                elif isinstance(c.value, str) and (
                    isinstance(Config.get_config(plugin.model, c.key, c.value), (list, tuple))
                    or isinstance(c.default_value, (list, tuple))
                ):
                    default_value = Config.get_config(plugin.model, c.key, c.value)
                    c.value = c.value.split(",")
                    if default_value and isinstance(default_value[0], int):
                        c.value = [int(x) for x in c.value]
                    elif default_value and isinstance(default_value[0], float):
                        c.value = [float(x) for x in c.value]
                    elif default_value and isinstance(default_value[0], bool):
                        temp = []
                        for x in c.value:
                            temp.append(x.lower() == "true")
                        c.value = temp
                Config.set_config(plugin.model, c.key, c.value)
            Config.save(None, True)
        else:
            if plugin.plugin_settings:
                for key, value in plugin.plugin_settings:
                    if key == "cmd":
                        value = value.split(",")
                    plugins2settings_manager.set_module_data(plugin.model, key, value)
            if plugin.plugin_manager:
                for key, value in plugin.plugin_manager:
                    plugins_manager.set_module_data(plugin.model, key, value)
    except Exception as e:
        logger.error(
            f"WEB_UI POST /webui/plugins model：{plugin.model} 发生错误 {type(e)}：{e}"
        )
        return Result(
            code=500,
            data=f"WEB_UI POST /webui/plugins model：{plugin.model} 发生错误 {type(e)}：{e}",
        )
    return Result(code=200, data="修改成功！")
