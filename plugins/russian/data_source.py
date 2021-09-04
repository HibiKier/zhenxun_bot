from models.russian_user import RussianUser
from utils.data_utils import init_rank


async def rank(group_id: int, itype) -> str:
    all_users = await RussianUser.get_all_user(group_id)
    all_user_id = [user.user_qq for user in all_users]
    if itype == 'win_rank':
        rank_name = '\t胜场排行榜\n'
        all_user_data = [user.win_count for user in all_users]
    elif itype == 'lose_rank':
        rank_name = '\t败场排行榜\n'
        all_user_data = [user.fail_count for user in all_users]
    elif itype == 'make_money':
        rank_name = '\t赢取金币排行榜\n'
        all_user_data = [user.make_money for user in all_users]
    elif itype == 'spend_money':
        rank_name = '\t输掉金币排行榜\n'
        all_user_data = [user.lose_money for user in all_users]
    elif itype == 'max_winning_streak':
        rank_name = '\t最高连胜排行榜\n'
        all_user_data = [user.max_winning_streak for user in all_users]
    else:
        rank_name = '\t最高连败排行榜\n'
        all_user_data = [user.max_losing_streak for user in all_users]
    rst = ''
    if all_users:
        rst = await init_rank(all_user_id, all_user_data, group_id)
    return rank_name + rst











