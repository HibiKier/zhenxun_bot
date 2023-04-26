from nonebot import on_notice,on_command,on_message
from nonebot.adapters.onebot.v11 import Bot,MessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandStart
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
import requests
import os
import pyzbar.pyzbar as pyzbar
import random
import cv2
import zxing
from configs.config import Config
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent,Message,Event,MessageSegment
import json

__zx_plugin_name__ = "二维码自动扫描"
__plugin_usage__ = """
usage：
    发图自动扫码
""".strip()
__plugin_des__ = "即时解码群聊出现的二维码"
__plugin_version__ = 0.1
__plugin_author__ = "Tokeii"
__plugin_task__ = {"qrcode": "自动扫码"}
__plugin_settings__ = {
    "level": 5,
    "default_status": False,
    "limit_superuser": False,
    
}
__plugin_type__ = ('工具',)

Config.add_plugin_config(
    "_task",
    "DEFAULT_QRdecode",
    False,
    help_="二维码自动解码 进群默认开关状态",
    default_value=False,
    type=bool,
)
# __plugin_block_limit__ = {
#     "check_type": "group",    # 'private'/'group'/'all'，限制私聊/群聊/全部
#     "limit_type": "717944543",   # 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
#     "rst": None,            # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
#     "status": True          # 此限制的开关状态
# }


temppath= 'qrCode/'

# QR_message = on_message(priority=5, block=False)
QR_message = on_command("scan", priority=5, block=True)
@QR_message.handle()

async def QR_message_(bot: Bot,event: MessageEvent,state: T_State):
    print("触发qrcode")
    msg = event.json()
    msg = json.loads(msg)
    print(type(msg))
    # print(str(event.json()))
    if [types['data']['url']  for types in msg['message'] if types['type']=='image']:

    # if "scan" in str(msg):
        

    # if str(event.message).split(',')[0]=='[CQ:image':
        # message_temp=str(event.message).split(',')
        url = [types['data']['url']  for types in msg['message'] if types['type']=='image'][0]
        print(url)

        #保存图片到本地
        try:
            r = requests.get(url)
            randomname = str(random.randint(1,100000000))+'.png'
            with open(temppath+randomname,'wb') as f:
                f.write(r.content)
                f.close()
                #解码二维码
                image = cv2.imread(temppath+randomname)
                # print(temppath+randomname)
                barcode = pyzbar.decode(image)
                reader1 = zxing.BarCodeReader()
                # print(reader1)
                barcode1 = reader1.decode(temppath+randomname)
                # print(barcode1)
            if barcode1.format!=None:
                await QR_message.finish(f"[+] 检测到{barcode1.format}码,已自动帮您解码"+Message("[CQ:face,id=320]")+'\n[+] '+barcode1.raw+'\ndecode by zxing')
            if barcode:
                qrtype =barcode[0].type
                #await bot.send_group_msg(group_id=event.group_id, message=f"[+] 检测到{qrtype}码,已自动帮您解码"+Message("[CQ:face,id=320]")+'\n[+] '+barcode[0].data.decode())
                #print(barcode[0].data.decode())
                await QR_message.finish(f"[+] 检测到{qrtype}码,已自动帮您解码"+Message("[CQ:face,id=320]")+'\n[+] '+barcode[0].data.decode()+'\ndecode by pyzbar')
                #删除文件
            else:
                # print("没扫出来")
                pass
        except Exception as e:
            error = ('错误明细是' + str(e.__class__.__name__) + str(e))
            if "Finished" in str(e.__class__.__name__):
                await QR_message.finish()
            if "TypeError" in str(e.__class__.__name__):
                await QR_message.finish()
            await QR_message.finish()
            logger.info(error)
        # 删除保存的图片
        try:
            os.remove(temppath+randomname)
            print("尝试删除")
            # pass
        except Exception as e:
            error = ('错误明细是' + str(e.__class__.__name__) + str(e))
            logger.info(error)
