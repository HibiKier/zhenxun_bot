class ForceAddGroupError(Exception):
    """
    强制拉群
    """

    def __init__(self, info: str):
        super().__init__(self)
        self._info = info

    def get_info(self) -> str:
        return self._info
