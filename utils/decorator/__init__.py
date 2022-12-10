class Singleton:

    """
    单例注解
    """

    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *args, **kw):
        if not hasattr(self, "_instance"):
            self._instance = self._cls(*args, **kw)
        return self._instance
