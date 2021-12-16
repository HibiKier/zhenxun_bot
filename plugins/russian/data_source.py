from .model import RussianUser
from typing import Optional
from utils.data_utils import init_rank
from utils.image_utils import BuildMat


async def rank(group_id: int, itype: str, num: int) -> Optional[BuildMat]:
    all_users = await RussianUser.get_all_user(group_id)
    all_user_id = [user.user_qq for user in all_users]
    if itype == 'win_rank':
        rank_name = '胜场排行榜'
        all_user_data = [user.win_count for user in all_users]
    elif itype == 'lose_rank':
        rank_name = '败场排行榜'
        all_user_data = [user.fail_count for user in all_users]
    elif itype == 'make_money':
        rank_name = '赢取金币排行榜'
        all_user_data = [user.make_money for user in all_users]
    elif itype == 'spend_money':
        rank_name = '输掉金币排行榜'
        all_user_data = [user.lose_money for user in all_users]
    elif itype == 'max_winning_streak':
        rank_name = '最高连胜排行榜'
        all_user_data = [user.max_winning_streak for user in all_users]
    else:
        rank_name = '最高连败排行榜'
        all_user_data = [user.max_losing_streak for user in all_users]
    rst = None
    if all_users:
        rst = await init_rank(rank_name, all_user_id, all_user_data, group_id, num)
    return rst











