from models.sigin_group_user import SignGroupUser


async def effect(user_id: int, group_id: int, name: str) -> bool:
    print(name)
    # try:
    if name == '好感双倍加持卡Ⅰ':
        user = await SignGroupUser.ensure(user_id, group_id)
        await user.update(
            add_probability=0.1
        ).apply()
    if name == '好感双倍加持卡Ⅱ':
        user = await SignGroupUser.ensure(user_id, group_id)
        await user.update(
            add_probability=0.2
        ).apply()
    if name == '好感双倍加持卡Ⅲ':
        user = await SignGroupUser.ensure(user_id, group_id)
        print(user.user_qq)
        await user.update(
            add_probability=0.3
        ).apply()
    return True
    # except Exception:
    #     return False















