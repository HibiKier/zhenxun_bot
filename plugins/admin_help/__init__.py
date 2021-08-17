from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent
from utils.image_utils import CreateImg
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from configs.config import NICKNAME


__plugin_name__ = '管理帮助 [Hidden]'
__plugin_usage__ = f'''管理帮助(权限等级)：
    1.更新群组成员列表(1)
    2.功能开关 --> 指令:开启/关闭xx功能(2)
    3.查看群被动技能 --> 指令:群通知状态(2)
    4.自定义群欢迎 --> 指令:自定义进群欢迎消息(2)
    5.将用户拉入{NICKNAME}黑名单 --> .ban/.unban(5)
    6.刷屏禁言相关 --> 指令:刷屏检测设置/设置检测时间
                        \t\t/设置检测次数/设置禁言时长(5)
    8.上传图片/连续上传图片(6) 
    9.移动图片(7)
    10.删除图片(7)
对我说 “{NICKNAME}帮助 指令” 获取对应详细帮助
群主与管理员默认 5 级权限
'''

passive_help = '''【被动技能开关(2)：
    开启/关闭早晚安
    开启/关闭进群欢迎
    开启/关闭每日开箱重置提醒
    开启/关闭b站转发解析
    开启/关闭丢人爬
    开启/关闭epic通知    
    开启/关闭原神黄历提醒
    开启/关闭全部通知】
'''

admin_help = on_command("管理员帮助", aliases={"管理帮助"}, priority=5, block=True)

admin_help_img = CreateImg(1000, 600, font_size=24)
admin_help_img.text((10, 10), __plugin_usage__)
text_img = CreateImg(450, 600, font_size=24)
text_img.text((0, 0), passive_help)
admin_help_img.paste(text_img, (650, 50))
admin_help_img.save(IMAGE_PATH + 'admin_help_img.png')


@admin_help.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await admin_help.send(image('admin_help_img.png'))
