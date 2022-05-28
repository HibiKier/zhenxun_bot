

def prompt2cn(text: str, count: int, s: str = "#") -> str:
    """
    格式化中文提示
    :param text: 文本
    :param count: 个数
    :param s: #
    """
    return s * count + "\n" + s * 6 + " " + text + " " + s * 6 + "\n" + s * count


