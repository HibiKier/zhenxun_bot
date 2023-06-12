import copy
from pathlib import Path
from typing import Any, Dict, Generic, NoReturn, Optional, TypeVar, Union

import ujson as json
from ruamel import yaml
from ruamel.yaml import YAML

from .models import *

_yaml = YAML(typ="safe")


T = TypeVar("T")


class StaticData(Generic[T]):
    """
    静态数据共享类
    """

    def __init__(self, file: Optional[Path], load_file: bool = True):
        self._data: dict = {}
        if file:
            file.parent.mkdir(exist_ok=True, parents=True)
            self.file = file
            if file.exists() and load_file:
                with open(file, "r", encoding="utf8") as f:
                    if file.name.endswith("json"):
                        try:
                            self._data: dict = json.load(f)
                        except ValueError:
                            if f.read().strip():
                                raise ValueError(f"{file} 文件加载错误，请检查文件内容格式.")
                    elif file.name.endswith("yaml"):
                        self._data = _yaml.load(f)

    def set(self, key, value):
        self._data[key] = value
        self.save()

    def set_module_data(self, module, key, value, auto_save: bool = True):
        if module in self._data.keys():
            self._data[module][key] = value
            if auto_save:
                self.save()

    def get(self, key) -> T:
        return self._data.get(key)

    def keys(self) -> List[str]:
        return self._data.keys()

    def delete(self, key):
        if self._data.get(key) is not None:
            del self._data[key]

    def get_data(self) -> Dict[str, T]:
        return copy.deepcopy(self._data)

    def dict(self) -> Dict[str, Any]:
        temp = {}
        for k, v in self._data.items():
            try:
                temp[k] = v.dict()
            except AttributeError:
                temp[k] = copy.deepcopy(v)
        return temp

    def save(self, path: Optional[Union[str, Path]] = None):
        path = path or self.file
        if isinstance(path, str):
            path = Path(path)
        if path:
            with open(path, "w", encoding="utf8") as f:
                if path.name.endswith("yaml"):
                    yaml.dump(
                        self._data,
                        f,
                        indent=2,
                        Dumper=yaml.RoundTripDumper,
                        allow_unicode=True,
                    )
                else:
                    json.dump(self.dict(), f, ensure_ascii=False, indent=4)

    def reload(self):
        if self.file.exists():
            if self.file.name.endswith("json"):
                self._data: dict = json.load(open(self.file, "r", encoding="utf8"))
            elif self.file.name.endswith("yaml"):
                self._data: dict = _yaml.load(open(self.file, "r", encoding="utf8"))

    def is_exists(self) -> bool:
        return self.file.exists()

    def is_empty(self) -> bool:
        return bool(len(self._data))

    def __str__(self) -> str:
        return str(self._data)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key) -> T:
        return self._data[key]

    def __len__(self) -> int:
        return len(self._data)
