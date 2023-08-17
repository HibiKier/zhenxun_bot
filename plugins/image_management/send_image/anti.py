import random
import warnings
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def pix_random_change(img):
    # Image转cv2
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img[0, 0, 0] = random.randint(0, 0xFFFFFFF)
    # cv2转Image
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return img


def pix_random_change_file(path: Path):
    # 注意：cv2.imread()不支持路径中文
    str_path = str(path.absolute())
    warnings.filterwarnings("ignore", category=Warning)
    img = cv2.imread(str_path)
    img[0, 0, 0] = random.randint(0, 0xFFFFFFF)
    cv2.imwrite(str_path, img)
    return str_path
