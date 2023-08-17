import cv2
import random
import warnings
import numpy as np
from PIL import Image


def pix_random_change(img):
    # Image转cv2
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img[0, 0, 0] = random.randint(0, 0xfffffff)
    # cv2转Image
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return img


def pix_random_change_file(path: str):
    # 注意：cv2.imread()不支持路径中文
    warnings.filterwarnings("ignore", category=Warning)
    img = cv2.imread(path)
    img[0, 0, 0] = random.randint(0, 0xfffffff)
    cv2.imwrite(path, img)

