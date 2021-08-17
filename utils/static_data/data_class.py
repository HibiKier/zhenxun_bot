from typing import Union
from pathlib import Path
import ujson as json


class StaticData:
    """
    静态数据共享类
    """

    def __init__(self, file: Path):
        file.parent.mkdir(exist_ok=True, parents=True)
        self.file = file
        self.data = {}
        if file.exists():
            self.data: dict = json.load(open(file, "r", encoding="utf8"))

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if self.data.get(key) is not None:
            del self.data[key]

    def save(self, path: Union[str, Path] = None):
        path = path if path else self.file
        with open(path, "w", encoding="utf8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def reload(self):
        if self.file.exists():
            self.data: dict = json.load(open(self.file, "r", encoding="utf8"))

    def is_exists(self):
        return self.file.exists()

    def is_empty(self):
        return bool(len(self.data))

    def __str__(self):
        return str(self.data)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

