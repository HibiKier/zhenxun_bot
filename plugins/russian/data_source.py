from models.russian_user import RussianUser
from utils.data_utils import init_rank


async def rank(group_id: int, itype) -> str:
    users = await RussianUser.all_user(group_id)
    if itype == 'win_rank':
        rank_name = '\t胜场排行榜\n'
        all_user_data = [user.win_count for user in users]
    elif itype == 'lose_rank':
        rank_name = '\t败场排行榜\n'
        all_user_data = [user.fail_count for user in users]
    elif itype == 'make_money':
        rank_name = '\t赢取金币排行榜\n'
        all_user_data = [user.make_money for user in users]
    else:
        rank_name = '\t输掉金币排行榜\n'
        all_user_data = [user.lose_money for user in users]
    rst = ''
    if users:
        rst = await init_rank(users, all_user_data, group_id)
    return rank_name + rst











