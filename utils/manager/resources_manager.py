from typing import Union, List, Optional
from .data_class import StaticData
from pathlib import Path
from ruamel.yaml import YAML
from services.log import logger
import shutil

yaml = YAML(typ="safe")


class ResourcesManager(StaticData):
    """
    插件配置 与 资源 管理器
    """

    def __init__(self, file: Path):
        self.file = file
        super().__init__(file)
        self._temp_dir = []
        self._abspath = Path()

    def add_resource(
        self, module: str, source_file: Union[str, Path], move_file: Union[str, Path]
    ):
        """
        添加一个资源移动路劲
        :param module: 模块名
        :param source_file: 源文件路径
        :param move_file: 移动路径
        """
        if isinstance(source_file, Path):
            source_file = str(source_file.absolute())
        if isinstance(move_file, Path):
            move_file = str(move_file.absolute())
        if module not in self._data.keys():
            self._data[module] = {source_file: move_file}
        else:
            self._data[module][source_file] = move_file

    def remove_resource(self, module: str, source_file: Optional[Union[str, Path]] = None):
        """
        删除一个资源路径
        :param module: 模块
        :param source_file: 源文件路径
        """
        if not source_file:
            if module in self._data.keys():
                for x in self._data[module].keys():
                    move_file = Path(self._data[module][x])
                    if move_file.exists():
                        shutil.rmtree(move_file.absolute(), ignore_errors=True)
                        logger.info(f"已清除插件 {module} 资源路径：{self._data[module][x]}")
                        del self._data[module][x]
        else:
            if isinstance(source_file, Path):
                source_file = str(source_file.absolute())
            if source_file:
                if module in self._data.keys() and source_file in self._data[module].keys():
                    move_file = Path(self._data[module][source_file])
                    if move_file.exists():
                        shutil.rmtree(move_file.absolute(), ignore_errors=True)
                    del self._data[module][source_file]
        self.save()

    def start_move(self):
        """
        开始移动路径
        """
        for module in self._data.keys():
            for source_path in self._data[module].keys():
                move_path = Path(self._data[module][source_path])
                try:
                    source_path = Path(source_path)
                    file_name = source_path.name
                    move_path = move_path / file_name
                    move_path.mkdir(exist_ok=True, parents=True)
                    if source_path.exists():
                        if move_path.exists():
                            shutil.rmtree(str(move_path.absolute()), ignore_errors=True)
                        shutil.move(str(source_path.absolute()), str(move_path.absolute()))
                        logger.info(
                            f"移动资源文件路径 {source_path.absolute()} >>> {move_path.absolute()}"
                        )
                    elif not move_path.exists():
                        logger.warning(
                            f"移动资源路径文件{source_path.absolute()} >>>"
                            f" {move_path.absolute()} 失败，源文件不存在.."
                        )
                except Exception as e:
                    logger.error(
                        f"移动资源路径文件{source_path.absolute()} >>>"
                        f" {move_path.absolute()}失败，{type(e)}：{e}"
                    )
        self.save()

    def add_temp_dir(self, path: Union[str, Path]):
        """
        添加临时清理文件夹
        :param path: 路径
        :param recursive: 是否将该目录下的所有目录也添加为临时文件夹
        """
        if isinstance(path, str):
            path = Path(path)
        self._temp_dir.append(path)

    def get_temp_data_dir(self) -> List[Path]:
        """
        获取临时文件文件夹
        """
        return self._temp_dir
