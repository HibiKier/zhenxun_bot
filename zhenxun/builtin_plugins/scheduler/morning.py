from nonebot_plugin_apscheduler import scheduler

# TODO: 消息发送

# # 早上好
# @scheduler.scheduled_job(
#     "cron",
#     hour=6,
#     minute=1,
# )
# async def _():
#     img = image(IMAGE_PATH / "zhenxun" / "zao.jpg")
#     await broadcast_group("[[_task|zwa]]早上好" + img, log_cmd="被动早晚安")
#     logger.info("每日早安发送...")


# # 睡觉了
# @scheduler.scheduled_job(
#     "cron",
#     hour=23,
#     minute=59,
# )
# async def _():
#     img = image(IMAGE_PATH / "zhenxun" / "sleep.jpg")
#     await broadcast_group(
#         f"[[_task|zwa]]{NICKNAME}要睡觉了，你们也要早点睡呀" + img, log_cmd="被动早晚安"
#     )
#     logger.info("每日晚安发送...")
