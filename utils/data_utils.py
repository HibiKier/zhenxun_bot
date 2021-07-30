from models.group_member_info import GroupInfoUser
from typing import List


async def init_rank(all_user_id: List[int], all_user_data: List[int], group_id: int) -> str:
    """
    说明：
        初始化通用的数据排行榜
    参数：
        :param all_user_id: 所有用户的qq号
        :param all_user_data: 所有用户需要排行的对应数据
        :param group_id: 群号，用于从数据库中获取该用户在此群的昵称
    """
    rst = ''
    for i in range(len(all_user_id) if len(all_user_id) < 10 else 10):
        _max = max(all_user_data)
        max_user_id = all_user_id[all_user_data.index(_max)]
        all_user_id.remove(max_user_id)
        all_user_data.remove(_max)
        try:
            user_name = (await GroupInfoUser.get_member_info(max_user_id, group_id)).user_name
        except AttributeError:
            user_name = f'{max_user_id}'
        rst += f'{user_name}: {_max}\n'
    return rst[:-1]






