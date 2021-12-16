from models.bag_user import BagUser
from utils.utils import is_number, get_user_avatar
from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
from .model import RedbagUser
import random
import os
from io import BytesIO
import asyncio


# 检查金币数量合法性，并添加记录数据
async def check_gold(user_id: int, group_id: int, amount: str):
    if is_number(amount):
        amount = int(amount)
        user_gold = await BagUser.get_gold(user_id, group_id)
        if amount < 1:
            return False, '小气鬼，要别人倒贴金币给你嘛！'
        if user_gold < amount:
            return False, '没有金币的话请不要发红包...'
        await BagUser.spend_gold(user_id, group_id, amount)
        await RedbagUser.add_redbag_data(user_id, group_id, 'send', amount)
        return True, amount
    else:
        return False, '给我好好的输入红包里金币的数量啊喂！'


# 金币退回
async def return_gold(user_id: int, group_id: int, amount: int):
    await BagUser.add_gold(user_id, group_id, amount)


# 开红包
async def open_redbag(user_id: int, group_id: int, redbag_data: dict):
    amount = random.choice(redbag_data[group_id]['redbag'])
    redbag_data[group_id]['redbag'].remove(amount)
    redbag_data[group_id]['open_user'].append(user_id)
    redbag_data[group_id]['open_amount'] += amount
    await RedbagUser.add_redbag_data(user_id, group_id, 'get', amount)
    await BagUser.add_gold(user_id, group_id, amount)
    return amount, redbag_data


# 随机红包图片
async def generate_send_redbag_pic(user_id: int, msg: str = '恭喜发财 大吉大利'):
    random_redbag = random.choice(os.listdir(f"{IMAGE_PATH}/prts/redbag_2"))
    redbag = BuildImage(0, 0, font_size=38, background=f'{IMAGE_PATH}/prts/redbag_2/{random_redbag}')
    ava = BuildImage(65, 65, background=BytesIO(await get_user_avatar(user_id)))
    await asyncio.get_event_loop().run_in_executor(None, ava.circle)
    redbag.text((int((redbag.size[0] - redbag.getsize(msg)[0]) / 2), 210), msg, (240, 218, 164))
    redbag.paste(ava, (int((redbag.size[0] - ava.size[0])/2), 130), True)
    return redbag.pic2bs4()


# 开红包图片
async def generate_open_redbag_pic(user_id: int, send_user_nickname: str, amount: int, text: str):
    return await asyncio.create_task(_generate_open_redbag_pic(user_id, send_user_nickname, amount, text))


# 开红包图片
async def _generate_open_redbag_pic(user_id: int, send_user_nickname: str, amount: int, text: str):
    send_user_nickname += '的红包'
    amount = str(amount)
    head = BuildImage(1000, 980, font_size=30, background=f'{IMAGE_PATH}/prts/redbag_12.png')
    size = BuildImage(0, 0, font_size=50).getsize(send_user_nickname)
    # QQ头像
    ava_bk = BuildImage(100 + size[0], 66, color='white', font_size=50)
    ava = BuildImage(66, 66, background=BytesIO(await get_user_avatar(user_id)))
    ava_bk.paste(ava)
    ava_bk.text((100, 7), send_user_nickname)
    # ava_bk.show()
    ava_bk_w, ava_bk_h = ava_bk.size
    head.paste(ava_bk, (int((1000 - ava_bk_w) / 2), 300))
    # 金额
    size = BuildImage(0, 0, font_size=150).getsize(amount)
    price = BuildImage(size[0], size[1], font_size=150)
    price.text((0, 0), amount, fill=(209, 171, 108))
    # 金币中文
    head.paste(price, (int((1000 - size[0]) / 2) - 50, 460))
    head.text((int((1000 - size[0]) / 2 + size[0]) - 50, 500 + size[1] - 70), '金币', fill=(209, 171, 108))
    # 剩余数量和金额
    head.text((350, 900), text, (198, 198, 198))
    return head.pic2bs4()



