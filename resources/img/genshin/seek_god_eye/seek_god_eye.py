
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO

import os
import json
import random
import base64

FILE_PATH = os.path.dirname(__file__)

JSON_LIST = ["风神瞳","岩神瞳"]



GOD_EYE_TOTAL = {
    # 每种神瞳有多少个，这个字典会在导入神瞳的json时初始化
    # "风神瞳" : 100
}

GOD_EYE_INFO = {
    # 所有神瞳的信息
    # "56": {
    #     "属性": "风神瞳",
    #     "gif_url": "https://uploadstatic.mihoyo.com/ys-obc/2020/09/21/76373921/cbd63e9fbb00160b045dafc424c1657f_1299454333660281584.gif",
    #     "备注": "",
    #     "x_pos": 1922.0018670150284,
    #     "y_pos": 683.9995073891628
    # }
}

GOD_EYE_CLASS_LIST = {
    # 每种神瞳的编号列表
    # "风神瞳":["1","2","3"],
    # "岩神瞳":["4","5","6"]

}


MAP_IMAGE = Image.open(os.path.join(FILE_PATH,"icon","map_icon.jpg"))
MAP_SIZE = MAP_IMAGE.size


# 风神瞳.json里记录的坐标是相对坐标，是以蒙德城的大雕像为中心的，所以图片合成时需要转换坐标
CENTER = (3505,1907)

# 神瞳位置图的裁切尺寸，默认是1000，表示图片长宽都是1000
CROP_SIZE = 1000

uid_info = {
    # 这个字典记录用户已经找到的神瞳编号
    # "12345":{
    #     "风神瞳":[],
    #     "岩神瞳":[]
    # }
}



for json_name in JSON_LIST:
    # 导入神瞳的.json文件
    with open(os.path.join(FILE_PATH, f"{json_name}.json"), 'r', encoding='UTF-8') as f:
        data = json.load(f)
        GOD_EYE_TOTAL[json_name] = len(data)
        GOD_EYE_INFO.update(data)
        GOD_EYE_CLASS_LIST.setdefault(json_name,list(data.keys()))




def save_uid_info():
    with open(os.path.join(FILE_PATH,'uid_info.json'),'w',encoding='UTF-8') as f:
        json.dump(uid_info,f,ensure_ascii=False,indent=4)


# 检查uid_info.json是否存在，没有创建空的
if not os.path.exists(os.path.join(FILE_PATH,'uid_info.json')):
    save_uid_info()

# 读取uid_info.json的信息
with open(os.path.join(FILE_PATH,'uid_info.json'),'r',encoding='UTF-8') as f:
    uid_info = json.load(f)





class God_eye_position_image(object):
    # 获取神瞳的位置图像
    # 传入的参数是神瞳的编号，实例化后直接调用get_cq_code即可返回图片的CQ码，使用base64发送
    def __init__(self,god_eye_id):
        self.id = str(god_eye_id)

        # ID对应的png文件名
        self.png_name = GOD_EYE_INFO[self.id]["属性"] + '.png'

        # 复制一份地图文件
        self.map_image = MAP_IMAGE.copy()

        # 神瞳的坐标
        self.x,self.y = self.transform_position()

        # 神瞳图片在paste时的偏移量
        self.offset = [50,120]

    def transform_position(self):
        # 风神瞳.json里记录的坐标是相对坐标,需要转换一下
        x = GOD_EYE_INFO[self.id]["x_pos"] + CENTER[0]
        y = GOD_EYE_INFO[self.id]["y_pos"] + CENTER[1]
        return [int(x),int(y)]

    def get_crop_pos(self):
        # 返回地图的裁切尺寸，检查裁切点是否越界
        x = max(self.x - CROP_SIZE/2,0)
        y = max(self.y - CROP_SIZE/2,0)
        r = min(self.x + CROP_SIZE/2,MAP_SIZE[0])
        l = min(self.y + CROP_SIZE/2,MAP_SIZE[1])
        return [x,y,r,l]

    def paste(self):
        # 把神瞳的图贴到地图上，然后以神瞳为中心裁切地图
        god_eye_image = Image.open(os.path.join(FILE_PATH, "icon", self.png_name))
        self.map_image.paste(god_eye_image,(self.x - self.offset[0],self.y - self.offset[1]),god_eye_image)
        self.map_image = self.map_image.crop(self.get_crop_pos())

    def get_cq_code(self):
        self.paste()
        bio = BytesIO()
        self.map_image.save(bio, format='JPEG')
        base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()

        return f"[CQ:image,file={base64_str}]"



class God_eye_map(object):

    def __init__(self,_resource_name,_uid,_mode = ""):
        self.resource_name = _resource_name
        self.uid = _uid
        self.mode = _mode

        # 地图要要裁切的左上角和右下角坐标
        # 这里初始化为地图的大小
        self.x_start = MAP_SIZE[0]
        self.y_start = MAP_SIZE[1]
        self.x_end = 0
        self.y_end = 0

        self.map_image = MAP_IMAGE.copy()

        self.resource_icon = Image.open(os.path.join(FILE_PATH,"icon",f"{self.resource_name}.png"))
        #self.resource_icon = self.resource_icon.resize((int(150*zoom),int(150*zoom)))


        self.resource_id_list = self.get_resource_point_list()


    def get_resource_point_list(self):

        temp_list = GOD_EYE_CLASS_LIST[self.resource_name].copy()

        if self.mode == "all":
            return temp_list

        for id in set(uid_info[self.uid][self.resource_name]):
            temp_list.remove(id)

        return temp_list


    def paste(self):
        for id in self.resource_id_list:
            # 把资源图片贴到地图上
            x = int(GOD_EYE_INFO[id]["x_pos"] + CENTER[0])
            y = int(GOD_EYE_INFO[id]["y_pos"] + CENTER[1])



            self.map_image.paste(self.resource_icon,(x - 50 , y - 120),self.resource_icon)

            draw = ImageDraw.Draw(self.map_image)
            setfont = ImageFont.truetype(FILE_PATH + '/Minimal.ttf', size=50)

            draw.text((x + 40, y - 60), str(id), fill="#000000", font=setfont)

            # 找出4个方向最远的坐标，用于后边裁切
            self.x_start = min(x,self.x_start)
            self.y_start = min(y,self.y_start)
            self.x_end = max(x,self.x_end)
            self.y_end = max(y,self.y_end)


    def crop(self):

        # 先把4个方向扩展150像素防止把资源图标裁掉
        self.x_start -= 150
        self.y_start -= 150
        self.x_end += 150
        self.y_end += 150

        # 如果图片裁切的太小会看不出资源的位置在哪，检查图片裁切的长和宽看够不够1000，不到1000的按1000裁切
        if (self.x_end - self.x_start)<1000:
            center = int((self.x_end + self.x_start) / 2)
            self.x_start = center - 500
            self.x_end  = center +500
        if (self.y_end - self.y_start)<1000:
            center = int((self.y_end + self.y_start) / 2)
            self.y_start = center - 500
            self.y_end  = center +500

        self.map_image = self.map_image.crop((self.x_start,self.y_start,self.x_end,self.y_end))

    def get_cq_cod(self):

        if not self.resource_id_list:
            return "没有这个资源的信息"

        self.paste()

        self.crop()

        bio = BytesIO()
        self.map_image.save(bio, format='JPEG')
        base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()

        return f"[CQ:image,file={base64_str}]"

    def get_resource_count(self):
        return len(self.resource_id_list)



def get_uid_number_found(uid:str):
    mes = "你找到的神瞳信息如下：\n"
    for eye_type in JSON_LIST:
        number = len(uid_info[uid][eye_type])
        mes += f"你已经找到了 {number} 个 {eye_type} ,该神瞳一共有 {GOD_EYE_TOTAL[eye_type]} 个!\n"
    return mes


def get_eye_gif_path(eye_id):
    # 获取gif的路径，找不到会返回空字符串
    eye_type = GOD_EYE_INFO[eye_id]["属性"]
    gif_path = os.path.join(FILE_PATH,"icon",eye_type,str(eye_id) + ".gif")
    if os.path.exists(gif_path):
        return gif_path
    else:
        return ""


def get_eye_gif_cq_code(eye_id):
    # 获取gif的CQ码，找不到gif文件会返回空字符串
    gif_path = get_eye_gif_path(eye_id)
    if gif_path == "":
        return ""

    gif_path = gif_path.replace("\\","/")
    cq_code = f'[CQ:image,file=file://{gif_path}]'
    return cq_code

def get_eye_remarks(eye_id):
    # 获取神瞳的备注，注意有的神瞳备注是空字符串
    return GOD_EYE_INFO[eye_id]["备注"]

def add_god_eye_info(uid,eye_id):
    eye_type = GOD_EYE_INFO[eye_id]["属性"]
    uid_info[uid][eye_type].append(eye_id)
    uid_info[uid][eye_type] = list(set(uid_info[uid][eye_type]))
    save_uid_info()

def init_uid_info(uid):
    # 初始化用户的信息
    if not (uid in uid_info):
        uid_info.setdefault(uid, {})
    for eye_type in JSON_LIST:
        if not (eye_type in uid_info[uid]):
            uid_info[uid].setdefault(eye_type, [])

def get_random_god_eye_id(uid,eye_type):
    # 获取一个随机没找到过的神瞳ID，返回随机到的神瞳ID，如果返回空字符串表示这种神瞳已经全部找到了
    if len(uid_info[uid][eye_type]) == GOD_EYE_TOTAL[eye_type]:
        return ""
    # 找出没找到过的神瞳列表
    temp_list = GOD_EYE_CLASS_LIST[eye_type].copy()

    for id in uid_info[uid][eye_type]:
        temp_list.remove(id)

    # eyes_never_found = set(GOD_EYE_CLASS_LIST[eye_type]).difference(set(uid_info[uid][eye_type]))
    # r = random.choice(list(eyes_never_found))
    r = random.choice(temp_list)
    return str(r)

def delete_god_eye_info(uid,eye_id):
    eye_type = GOD_EYE_INFO[eye_id]["属性"]
    if not (eye_id in uid_info[uid][eye_type]):
        return "你还没有找到这个神瞳！"

    uid_info[uid][eye_type].remove(eye_id)
    save_uid_info()
    return f"已经在你的记录列表删除编号为 {eye_id} 的神瞳"

def reset_god_eye_info(uid,eye_type):
    # 重置某一种神瞳的已找到列表
    uid_info[uid][eye_type].clear()
    save_uid_info()
    return "已重置已找到这种神瞳的列表"

def get_god_eye_message(eye_id):
    message = f"当前神瞳编号 {eye_id} \n"
    message += God_eye_position_image(eye_id).get_cq_code() # 获取神瞳位置图
    message += "\n"

    gif_cq_code = get_eye_gif_cq_code(eye_id) # 获取找神瞳的动图，没有找到这就是个空字符串
    if gif_cq_code:
        message += gif_cq_code
        message += "\n"

    remarks_txt = get_eye_remarks(eye_id) # 获取神瞳的备注信息
    if remarks_txt:
        message += "备注："
        message += remarks_txt
        message += "\n"

    message += "\n※ 如果你找到了神瞳或者你确定这个神瞳已经找过了，可以发送 找到神瞳了 神瞳编号\n"
    message += "※ 机器人记录你找到这个神瞳之后将不再给你发送这个神瞳位置\n"
    message += "※ 图片及数据来源于原神观测枢wiki\n"
    message += "※ 神瞳位置有可能有细微误差，具体以游戏里为准"

    return message

def found_god_eye(uid,eye_id):
    add_god_eye_info(uid,eye_id)
    save_uid_info()
    return f"已添加编号为 {eye_id} 的神瞳找到记录！"



def all_god_eye_map(uid,eye_type,mode = ""):
    mes = "神之眼信息如下：\n"

    mes += God_eye_map(eye_type,uid,mode).get_cq_cod()

    return mes

