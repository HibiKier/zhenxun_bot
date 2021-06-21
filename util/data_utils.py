from models.group_member_info import GroupInfoUser


# 生成通用排行榜
async def init_rank(users: list, all_user_data: list, group_id: int):
    all_user_id = [user.user_qq for user in users]
    rst = ''
    for i in range(len(all_user_id) if len(all_user_id) < 10 else 10):
        _max = max(all_user_data)
        max_user_id = all_user_id[all_user_data.index(_max)]
        all_user_id.remove(max_user_id)
        all_user_data.remove(_max)
        try:
            user_name = (await GroupInfoUser.select_member_info(max_user_id, group_id)).user_name
        except AttributeError:
            user_name = f'{max_user_id}'
        rst += f'{user_name}: {_max}\n'
    return rst[:-1]






