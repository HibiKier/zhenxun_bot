# from typing import Optional, Any
# from .data_class import StaticData
# from pathlib import Path
# from ruamel.yaml import YAML
#
# yaml = YAML(typ="safe")
#
#
# class ConfigsManager(StaticData):
#     """
#     插件配置 与 资源 管理器
#     """
#
#     def __init__(self, file: Path):
#         self.file = file
#         super().__init__(file)
#         self._resource_data = {}
#
#     def add_plugin_config(
#         self,
#         module: str,
#         key: str,
#         value: str,
#         help_: Optional[str] = None,
#         default_value: Optional[str] = None,
#     ):
#         """
#         为插件添加一个配置
#         :param module: 模块
#         :param key: 键
#         :param value: 值
#         :param help_: 配置注解
#         :param default_value: 默认值
#         """
#         if self._data.get(module) is None:
#             self._data[module] = {}
#         self._data[module][key] = {
#             "value": value,
#             "help": help_,
#             "default_value": default_value,
#         }
#
#     def remove_plugin_config(self, module: str):
#         """
#         为插件删除一个配置
#         :param module: 模块名
#         """
#         if module in self._data.keys():
#             del self._data[module]
#
#     def get_config(self, module: str, key: str) -> Optional[Any]:
#         """
#         获取指定配置值
#         :param module: 模块名
#         :param key: 配置名称
#         """
#         if module in self._data.keys():
#             if self._data[module].get(key):
#                 if self._data[module][key]["value"] is None:
#                     return self._data[module][key]["default_value"]
#                 return self._data[module][key]["value"]
#         return None
#
#
#
