from typing import Union, Optional
from pathlib import Path
from ruamel.yaml import YAML
import ujson as json

yaml = YAML(typ="safe")


class StaticData:
    """
    静态数据共享类
    """

    def __init__(self, file: Optional[Path]):
        self._data: dict = {}
        if file:
            file.parent.mkdir(exist_ok=True, parents=True)
            self.file = file
            if file.exists():
                with open(file, "r", encoding="utf8") as f:
                    if file.name.endswith("json"):
                        try:
                            self._data: dict = json.load(f)
                        except ValueError:
                            if f.read().strip():
                                raise ValueError(f"{file} 文件加载错误，请检查文件内容格式.")
                    elif file.name.endswith("yaml"):
                        self._data = yaml.load(f)

    def set(self, key, value):
        self._data[key] = value
        self.save()

    def set_module_data(self, module, key, value):
        if module in self._data.keys():
            self._data[module][key] = value
        self.save()

    def get(self, key):
        return self._data.get(key)

    def keys(self):
        return self._data.keys()

    def delete(self, key):
        if self._data.get(key) is not None:
            del self._data[key]

    def get_data(self) -> dict:
        return self._data

    def save(self, path: Union[str, Path] = None):
        path = path if path else self.file
        if isinstance(path, str):
            path = Path(path)
        if path:
            with open(path, "w", encoding="utf8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=4)

    def reload(self):
        if self.file.exists():
            if self.file.name.endswith("json"):
                self._data: dict = json.load(open(self.file, "r", encoding="utf8"))
            elif self.file.name.endswith("yaml"):
                self._data: dict = yaml.load(open(self.file, "r", encoding="utf8"))

    def is_exists(self):
        return self.file.exists()

    def is_empty(self):
        return bool(len(self._data))

    def __str__(self):
        return str(self._data)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]
