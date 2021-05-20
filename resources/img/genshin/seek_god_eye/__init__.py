from hoshino import Service
from nonebot import on_command
# from ..config import ALLOW_PRIVATE_CHAT
import random
from .seek_god_eye import (JSON_LIST,
                           GOD_EYE_INFO,
                           GOD_EYE_CLASS_LIST,
                           init_uid_info,
                           get_random_god_eye_id,
                           get_god_eye_message,
                           get_uid_number_found,
                           found_god_eye,
                           all_god_eye_map,
                           delete_god_eye_info,
                           reset_god_eye_info)






sv = Service('原神神瞳信息查询')

search_god_eye_command = []
for eye_type in JSON_LIST:
    search_god_eye_command.append(f"找{eye_type}")

reset_god_eye_command = []
for eye_type in JSON_LIST:
    reset_god_eye_command.append(f"重置{eye_type}找到记录")

verification_code_list = {
    # 重置已找到神瞳列表时需要二次确认，这个字典用来存验证码
    # "QQ号" : 验证码
}


@sv.on_prefix(search_god_eye_command)
async def search_god_eye(bot, ev):

    command_txt = ev['prefix']
    god_eye_id = ev.message.extract_plain_text().strip()
    userid = str(ev['user_id'])
    init_uid_info(userid)

    if not (god_eye_id in GOD_EYE_INFO):
        if god_eye_id != "":
            await bot.send(ev, f"找不到编号为 {god_eye_id} 的神瞳" , at_sender=True)
            return

    god_eye_type = command_txt[1:] # 把指令前边的 找 字去掉

    if god_eye_id == "":
        # 如果用户没有给神瞳ID就根据属性随机一个没找到过的返回
        god_eye_id = get_random_god_eye_id(userid,god_eye_type)

    if god_eye_id == "":
        # 如果随机之后还是空字符串，就表示这种神瞳已经都找完了
        await bot.send(ev, f"你已经找完这种神瞳了！", at_sender=True)
        return

    mes = get_god_eye_message(god_eye_id)

    await bot.send(ev, mes, at_sender=True)



@sv.on_prefix("找到神瞳了")
async def found_it(bot, ev):
    god_eye_id = ev.message.extract_plain_text().strip()
    userid = str(ev['user_id'])
    init_uid_info(userid)

    if god_eye_id == "":
        await bot.send(ev, f"你需要发送一个神瞳编号" , at_sender=True)
        return

    if not (god_eye_id in GOD_EYE_INFO):
        await bot.send(ev, f"找不到编号为 {god_eye_id} 的神瞳" , at_sender=True)
        return

    mes = found_god_eye(userid,god_eye_id)

    await bot.send(ev, mes, at_sender=True)



@sv.on_prefix("删除找到神瞳",only_to_me=True)
async def delete_god_eye_id(bot, ev):

    god_eye_id = ev.message.extract_plain_text().strip()
    userid = str(ev['user_id'])
    init_uid_info(userid)

    if god_eye_id == "":
        await bot.send(ev, f"你需要发送一个神瞳编号" , at_sender=True)
        return

    if not (god_eye_id in GOD_EYE_INFO):
        await bot.send(ev, f"找不到编号为 {god_eye_id} 的神瞳" , at_sender=True)
        return

    mes = delete_god_eye_info(userid,god_eye_id)

    await bot.send(ev, mes, at_sender=True)


@sv.on_prefix(reset_god_eye_command,only_to_me=True)
async def reset_god_eye_(bot, ev):

    verification_code = ev.message.extract_plain_text().strip()
    userid = (ev['user_id'])
    init_uid_info(userid)
    command_txt = ev['prefix'].strip()
    god_eye_type = command_txt[2:-4]

    if not (god_eye_type in JSON_LIST):
        await bot.send(ev, f"没有这种神瞳" , at_sender=True)
        return

    if verification_code == "":

        new_verification_code = ""
        for i in range(4):
            # 生成一个4位的字母验证码
            new_verification_code += str(chr(random.randint(65,90)))

        verification_code_list[userid] = new_verification_code
        await bot.send(ev, f"你确定要重置已经找到的神瞳记录吗？如果确定请发送：\n{command_txt}{new_verification_code}" , at_sender=True)
        return


    if verification_code_list[userid] == verification_code:
        reset_god_eye_info(userid,god_eye_type)
        verification_code_list.pop(userid)
        await bot.send(ev, f"已重置已经找到的{god_eye_type}记录" , at_sender=True)
        return

    await bot.send(ev, f"验证码错误，请检查验证码是否正确或重新生成验证码。", at_sender=True)



@sv.on_prefix("找到多少神瞳了",only_to_me=True)
async def found_god_eye_info(bot, ev):
    userid = str(ev['user_id'])
    init_uid_info(userid)

    mes = get_uid_number_found(userid)

    await bot.send(ev, mes, at_sender=True)



@sv.on_prefix("没找到的",only_to_me=True)
async def not_found_god_eye_info(bot, ev):
    userid = str(ev['user_id'])
    init_uid_info(userid)
    god_eye_type = ev.message.extract_plain_text().strip()

    if not (god_eye_type in JSON_LIST):
        await bot.send(ev, f"没有这种神瞳" , at_sender=True)
        return

    await bot.send(ev, all_god_eye_map(userid,god_eye_type,""), at_sender=True)



@sv.on_prefix("所有的",only_to_me=True)
async def not_found_god_eye_info(bot, ev):
    userid = str(ev['user_id'])
    init_uid_info(userid)
    god_eye_type = ev.message.extract_plain_text().strip()

    if not (god_eye_type in JSON_LIST):
        await bot.send(ev, f"没有这种神瞳" , at_sender=True)
        return

    await bot.send(ev, all_god_eye_map(userid,god_eye_type,"all"), at_sender=True)