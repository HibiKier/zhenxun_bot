from strenum import StrEnum


class ImageHandleType(StrEnum):
    """
    图片处理类型
    """

    UPLOAD = "UPLOAD"
    """上传"""
    DELETE = "DELETE"
    """删除"""
    MOVE = "MOVE"
    """移动"""
