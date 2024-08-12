class InformationContainer:
    def __init__(
        self,
        vd_info=None,
        live_info=None,
        vd_url=None,
        live_url=None,
        image_info=None,
        image_url=None,
    ):
        self._vd_info = vd_info
        self._live_info = live_info
        self._vd_url = vd_url
        self._live_url = live_url
        self._image_info = image_info
        self._image_url = image_url

    @property
    def vd_info(self):
        return self._vd_info

    @property
    def live_info(self):
        return self._live_info

    @property
    def vd_url(self):
        return self._vd_url

    @property
    def live_url(self):
        return self._live_url

    @property
    def image_info(self):
        return self._image_info

    @property
    def image_url(self):
        return self._image_url

    def update(self, updates):
        """
        更新多个信息的通用方法
        Args:
            updates (dict): 包含信息类型和对应新值的字典
        """
        for info_type, new_value in updates.items():
            if hasattr(self, f"_{info_type}"):
                setattr(self, f"_{info_type}", new_value)

    def get_information(self):
        return self
