import os
import imagehash
from PIL import Image
try:
    import ujson as json
except ModuleNotFoundError:
    import json

IMAGE_PATH = r"/home/hibiki/hibikibot/resources/img/"
TXT_PATH = r"/home/hibiki/hibikibot/resources/txt/"


def get_img_hash(image_file):
    with open(image_file, 'rb') as fp:
        hash_value = imagehash.average_hash(Image.open(fp))
    return hash_value


def check_file_index():
    for dir_name in ['setu/', 'r18/']:
        lens = len(os.listdir(IMAGE_PATH + dir_name))
        for i in range(lens):
            if i > lens:
                return
            if not os.path.exists(f"{IMAGE_PATH}{dir_name}{i}.jpg"):
                os.rename(f"{IMAGE_PATH}{dir_name}{lens}.jpg", f"{IMAGE_PATH}{dir_name}{i}.jpg")
                print(f'{lens}.jpg --> {i}.jpg')
                lens -= 1
            if not i % 100:
                print(f'已检测 {i} 份数据')
        print(f'{dir_name} 检测完毕')


def check_setu_hash():
    check_file_index()
    for dir_name in ['setu/', 'r18/']:
        img_data = {}
        if dir_name == 'setu/':
            fn = 'setu_img_hash.json'
        else:
            fn = 'r18_setu_img_hash.json'
        file_list_len = len(os.listdir(IMAGE_PATH + dir_name)) - 1
        print(file_list_len)
        for i in range(file_list_len):
            file = f"{i}.jpg"
            index = file.split(".")[0]
            img_hash = str(get_img_hash(IMAGE_PATH + dir_name + file))
            print(f'{index}.jpg --> {img_hash}')
            if img_hash in img_data.values():
                k = [k for k, v in img_data.items() if v == img_hash]
                print(f'文件 {index}.jpg 与 {k}.jpg 重复，使用 {file_list_len}.jpg 进行替换')
                os.remove(IMAGE_PATH + dir_name + file)
                os.rename(IMAGE_PATH + f'{dir_name}{file_list_len}.jpg', IMAGE_PATH + dir_name + file)
                file_list_len -= 1
                continue
            img_data[index] = img_hash
        # print(f'{index}.jpg --> {img_data}')
        with open(TXT_PATH + fn, 'w') as f:
            json.dump(img_data, f, indent=4)


check_setu_hash()