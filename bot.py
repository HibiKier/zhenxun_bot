import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from services.db_context import init, disconnect
nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
config = driver.config
driver.on_startup(init)
driver.on_shutdown(disconnect)
nonebot.load_builtin_plugins()
nonebot.load_plugins("plugins")
nonebot.load_plugins("plugins/shop")
nonebot.load_plugins("plugins/genshin")


if __name__ == "__main__":
    nonebot.run()














# None
# ---------------------
# 775757368                     print(event.get_user_id())
# 775757368                     print(event.get_session_id())
# 天气                           print(event.get_message())
# message.group.normal          print(event.get_event_name())
# 天气                            print(event.get_plaintext())
# -------
# 863633108                     print(event.group_id)
# 775757368                     print(event.user_id)
# 1851212230                    print(event.message_id)

# event
# [request.group.invite]: {
# 'time': 1612430661, 'self_id': 3054557284, 'post_type': 'request', 'request_type': 'group', 'sub_type': 'invite',
# 'group_id': 863633108, 'user_id': 775757368, 'comment': '', 'flag': '1612430661235986'}

# [request.friend]: {'time': 1612431762, 'self_id': 3054557284, 'post_type': 'request',
# 'request_type': 'friend', 'user_id': 3238573864, 'comment': '', 'flag': '1612431762000000'}


# [notice.group_decrease.leave]: {'time': 1612620312,
# 'self_id': 3054557284, 'post_type': 'notice', 'notice_type': 'group_decrease',
# 'sub_type': 'leave', 'user_id': 3238573864, 'group_id': 863633108, 'operator_id': 3238573864}

# [notice.group_increase.approve]: {'time': 1612620506,
# 'self_id': 3054557284, 'post_type': 'notice', 'notice_type': 'group_increase',
# 'sub_type': 'approve', 'user_id': 3238573864, 'group_id': 863633108, 'operator_id': 0}

# get_group_list
# [{'group_id': 210287674, 'group_name': '豪爹头号粉丝⑧群', 'max_member_count': 200, 'member_count': 14},
# {'group_id': 863633108, 'group_name': 'Amireux、这里是、可…', 'max_member_count': 200, 'member_count': 4}]

# 消息event
# {"time": 1613886297, "self_id": 3054557284, "post_type": "message", "sub_type": "normal", "user_id": 3238573864,
# "message_type": "group", "message_id": 1933353523, "message": [{"type": "text", "data": {"text": "666"}}],
# "raw_message": "A666", "font": 0, "sender": {"user_id": 3238573864, "nickname":
# "\u53ef\u7231\u7684\u5c0f\u771f\u5bfb", "sex": "unknown", "age": 0, "card": "", "area": "", "level": "",
# "role": "member/admin/owner", "title": ""}, "to_me": true, "reply": null, "group_id": 863633108, "anonymous": null}

# bilibili转发
# {"app":"com.tencent.miniapp_01","config":{"autoSize":0,"ctime":1613992391,"forward":1,"height":0,"
# token":"f7f529900be6af62f4d864f8a92c94c9","type":"normal","width":0},"desc":"哔哩哔哩",
# "extra":{"app_type":1,"appid":100951776,"uin":775757368},"meta":{"detail_1":{"appid":"1109937557",
# "desc":"B 站 用 户 三 连 现 状","gamePoints":"","gamePointsUrl":"","host":{"nick":"这里是","uin":775757368},
# "icon":"http://miniapp.gtimg.cn/public/appicon/432b76be3a548fc128acaa6c1ec90131_200.jpg",
# "preview":"pubminishare-30161.picsz.qpic.cn/4f5a19fb-42d5-4bb5-bc0a-b92fa5a06519",
# "qqdocurl":"https://b23.tv/qDvchc?share_medium=android&share_source=qq&bbid=XYDEA6CD35717661AE594D9DD99A5E852E414&ts=1613992387314",
# "scene":1036,"shareTemplateData":{},"shareTemplateId":"8C8E89B49BE609866298ADDFF2DBABA4","showLittleTail":"","title":"哔哩哔哩",
# "url":"m.q.qq.com/a/s/130c1f9c2af58430805ebfda192caa9a"}},"needShareCallBack":false,"prompt":"[QQ小程序]哔哩哔哩","ver":"1.0.0.19",
# "view":"view_8C8E89B49BE609866298ADDFF2DBABA4"}

#event
# [notice.group_decrease.kick_me]: {'time': 1614143313, 'self_id': 3054557284, 'post_type': 'notice',
# 'notice_type': 'group_decrease', 'sub_type': 'kick_me', 'user_id': 3054557284, 'group_id': 863633108,
# 'operator_id': 775757368}

# [request.group.add]: {'time': 1614851972, 'self_id': 3238573864, 'post_type': 'request', 'request_type': 'group',
# 'sub_type': 'add', 'group_id': 774261838, 'user_id': 3054557284, 'comment': '问题：为啥加群鸭？\n答案：哈哈哈',
# 'flag': '1614851972274444'}



