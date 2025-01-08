from zhenxun.configs.config import Config
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.utils.enum import PluginType
from zhenxun.utils.utils import FreqLimiter

base_config = Config.get("hook")


class FreqUtils:
    def __init__(self):
        check_notice_info_cd = Config.get_config("hook", "CHECK_NOTICE_INFO_CD")
        if check_notice_info_cd is None or check_notice_info_cd < 0:
            raise ValueError("模块: [hook], 配置项: [CHECK_NOTICE_INFO_CD] 为空或小于0")
        self._flmt = FreqLimiter(check_notice_info_cd)
        self._flmt_g = FreqLimiter(check_notice_info_cd)
        self._flmt_s = FreqLimiter(check_notice_info_cd)
        self._flmt_c = FreqLimiter(check_notice_info_cd)

    def is_send_limit_message(
        self, plugin: PluginInfo, sid: str, is_poke: bool
    ) -> bool:
        """是否发送提示消息

        参数:
            plugin: PluginInfo
            sid: 检测键
            is_poke: 是否是戳一戳

        返回:
            bool: 是否发送提示消息
        """
        if is_poke:
            return False
        if not base_config.get("IS_SEND_TIP_MESSAGE"):
            return False
        if plugin.plugin_type == PluginType.DEPENDANT:
            return False
        return plugin.module != "ai" if self._flmt_s.check(sid) else False


freq = FreqUtils()
