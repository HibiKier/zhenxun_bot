class NetworkError(Exception):
    pass


class PlatformUnsupportError(Exception):
    def __init__(self, platform: str):
        self.platform = platform
