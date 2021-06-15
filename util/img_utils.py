import os
from configs.path_config import IMAGE_PATH, TXT_PATH, TTF_PATH
from PIL import Image, ImageFile, ImageDraw, ImageFont
import cv2
import imagehash
import base64
from io import BytesIO
from matplotlib import pyplot as plt


# 扫描图库id是否连贯
def scan_img(path):
    path = IMAGE_PATH + path
    nolist = []
    length = len(os.listdir(path))
    print(length)
    for i in range(length):
        if i in nolist:
            continue
        img_path = path + "{}.jpg".format(i)
        if not os.path.exists(img_path):
            print("不存在=== " + str(length) + ".jpg -------> " + str(i) + ".jpg")
            os.rename(path + "{}.jpg".format(length - 1), img_path)
            nolist.append(length)
            length -= 1


# 比较hash值
def compare_image_with_hash(image_file1, image_file2, max_dif=1.5):
    """
    max_dif: 允许最大hash差值, 越小越精确,最小为0
    推荐使用
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    hash_1 = None
    hash_2 = None
    hash_1 = get_img_hash(image_file1)
    hash_2 = get_img_hash(image_file2)
    dif = hash_1 - hash_2
    if dif < 0:
        dif = -dif
    if dif <= max_dif:
        return True
    else:
        return False


# 比较图片与hash值
def compare_one_img_hash(image_file, hash_2, max_dif=1.5):
    hash_1 = get_img_hash(image_file)
    dif = hash_1 - hash_2
    if dif < 0:
        dif = -dif
    if dif <= max_dif:
        return True
    else:
        return False


def get_img_hash(image_file):
    with open(image_file, 'rb') as fp:
        hash_value = imagehash.average_hash(Image.open(fp))
    return hash_value


# 压缩图片
def rar_imgs(inpath, outpath, ratio=0.9, start=0, end=0, lens=0, maxsize=0.0, in_file_name='', out_file_name='',
             itype='jpg'):
    in_path = IMAGE_PATH + inpath + '/'
    out_path = IMAGE_PATH + outpath + '/'
    # scan_img(inpath)
    l = []
    if in_file_name != '' and out_file_name != '':
        filein = in_path + in_file_name + "." + itype
        fileout = out_path + out_file_name + "." + itype
        h, w, d = cv2.imread(filein).shape
        width = int(w * ratio)
        height = int(h * ratio)
        ResizeImage(filein, fileout, width, height)
    else:
        if lens == 0:
            lens = len(os.listdir(in_path))
        if end == 0:
            end = lens
        for i in range(start, end):
            if i in l:
                continue
            if maxsize != 0:
                if os.path.getsize(in_path + str(i) + ".jpg") > maxsize:
                    print("压缩----->", i, ".jpg")
                    filein = in_path + str(i) + ".jpg"
                    fileout = out_path + str(i) + ".jpg"
                    h, w, d = cv2.imread(filein).shape
                    width = int(w * ratio)
                    height = int(h * ratio)
                    ResizeImage(filein, fileout, width, height)
                else:
                    continue
            else:
                print("压缩----->", i, ".jpg")
                filein = in_path + str(i) + ".jpg"
                fileout = out_path + str(i) + ".jpg"
                h, w, d = cv2.imread(filein).shape
                width = int(w * ratio)
                height = int(h * ratio)
                ResizeImage(filein, fileout, width, height)


# 压缩
def ResizeImage(filein, fileout, width, height):
    img = cv2.resize(cv2.imread(filein), (int(width), int(height)))
    cv2.imwrite(fileout, img)


# 保存图片压缩后的hash值
def save_img_hash(path, name):
    for file in os.listdir(IMAGE_PATH + path):
        if os.path.getsize(IMAGE_PATH + path + file) > 1024 * 1024 * 1.5:
            compare_img_hash_in_txt(IMAGE_PATH + 'rar/' + file, name)
        else:
            compare_img_hash_in_txt(IMAGE_PATH + path + file, name)


# 比较色图hash值
def compare_img_hash_in_txt(file, name, mode=1):
    with open(TXT_PATH + name + ".txt", 'a+') as txtfile:
        txtfile.seek(0)
        hash_list = txtfile.read()[:-1].strip(",")
        txtfile.seek(2)
        with open(file, 'rb') as fp:
            img_hash = str(imagehash.average_hash(Image.open(fp)))
            if img_hash not in hash_list:
                if mode == 1:
                    txtfile.write(img_hash + ",")
                return False
    return True


# 透明背景 -> 白色
def alphabg2white_PIL(img):
    img = img.convert('RGBA')
    sp = img.size
    width = sp[0]
    height = sp[1]
    for yh in range(height):
        for xw in range(width):
            dot = (xw, yh)
            color_d = img.getpixel(dot)
            if color_d[3] == 0:
                color_d = (255, 255, 255, 255)
                img.putpixel(dot, color_d)
    return img


def pic2b64(pic: Image) -> str:
    buf = BytesIO()
    pic.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return 'base64://' + base64_str


def fig2b64(plt: plt) -> str:
    buf = BytesIO()
    plt.savefig(buf, format='PNG', dpi=100)
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return 'base64://' + base64_str


class CreateImg:
    def __init__(self,
                 w,
                 h,
                 img_w=0,
                 img_h=0,
                 color='white',
                 image_type='RGBA',
                 font_size=10,
                 background='',
                 ttf='yz.ttf',
                 divisor=1):
        self.w = int(w)
        self.h = int(h)
        self.img_w = int(img_w)
        self.img_h = int(img_h)
        self.current_w = 0
        self.current_h = 0
        self.ttfont = ImageFont.truetype(TTF_PATH + ttf, int(font_size))
        if not background:
            self.markImg = Image.new(image_type, (self.w, self.h), color)
        else:
            if w == 0 and h == 0:
                self.markImg = Image.open(background)
                w, h = self.markImg.size
                if divisor:
                    self.w = int(divisor * w)
                    self.h = int(divisor * h)
                    self.markImg = self.markImg.resize((self.w, self.h), Image.ANTIALIAS)
                else:
                    self.w = w
                    self.h = h
            else:
                self.markImg = Image.open(background).resize((self.w, self.h), Image.ANTIALIAS)
        self.draw = ImageDraw.Draw(self.markImg)
        self.size = self.w, self.h

    # 贴图
    def paste(self, img, pos=None, alpha=False):
        if isinstance(img, CreateImg):
            img = img.markImg
        if self.current_w == self.w:
            self.current_w = 0
            self.current_h += self.img_h
        if not pos:
            pos = (self.current_w, self.current_h)
        if alpha:
            try:
                self.markImg.paste(img, pos, img)
            except ValueError:
                img = img.convert("RGBA")
                self.markImg.paste(img, pos, img)
        else:
            self.markImg.paste(img, pos)
        self.current_w += self.img_w
        return self.markImg

    # 获取文字大小
    def getsize(self, msg):
        return self.ttfont.getsize(msg)

    # 写字
    def text(self, pos, text, fill=(0, 0, 0)):
        self.draw.text(pos, text, fill=fill, font=self.ttfont)
        return self.markImg

    # 饼图
    def pieslice(self):
        self.draw.pieslice((350, 50, 500, 200), -150, -30, 'pink', 'crimson')
        return self.markImg

    # 保存
    def save(self, path):
        self.markImg.save(path)

    # 显示
    def show(self):
        self.markImg.show(self.markImg)

    # 压缩
    def resize(self, ratio=0, w=0, h=0):
        if not w and not h and not ratio:
            raise Exception('缺少参数...')
        if not w and not h and ratio:
            w = int(self.w * ratio)
            h = int(self.h * ratio)
        self.markImg = self.markImg.resize((w, h), Image.ANTIALIAS)
        self.w, self.h = self.markImg.size
        self.size = self.w, self.h
        self.draw = ImageDraw.Draw(self.markImg)

    # 检查字体大小
    def check_font_size(self, word):
        return self.ttfont.getsize(word)[0] > self.w

    # 透明化
    def transparent(self, n=0):
        self.markImg = self.markImg.convert('RGBA')  # 修改颜色通道为RGBA
        x, y = self.markImg.size     # 获得长和宽
        # 设置每个像素点颜色的透明度
        for i in range(n, x - n):
            for k in range(n, y - n):
                color = self.markImg.getpixel((i, k))
                color = color[:-1] + (100, )
                self.markImg.putpixel((i, k), color)
        return self.markImg

    # 转bs4:
    def pic2bs4(self):
        buf = BytesIO()
        self.markImg.save(buf, format='PNG')
        base64_str = base64.b64encode(buf.getvalue()).decode()
        return base64_str

    #
    def convert(self, itype):
        self.markImg = self.markImg.convert(itype)

    # 变圆
    def circle(self):
        self.convert('RGBA')
        r2 = min(self.w, self.h)
        if self.w != self.h:
            self.resize(w=r2, h=r2)
        r3 = int(r2 / 2)
        imb = Image.new('RGBA', (r3 * 2, r3 * 2), (255, 255, 255, 0))
        pima = self.markImg.load()  # 像素的访问对象
        pimb = imb.load()
        r = float(r2 / 2)
        for i in range(r2):
            for j in range(r2):
                lx = abs(i - r)  # 到圆心距离的横坐标
                ly = abs(j - r)  # 到圆心距离的纵坐标
                l = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径
                if l < r3:
                    pimb[i - (r - r3), j - (r - r3)] = pima[i, j]
        self.markImg = imb



if __name__ == '__main__':
    pass












