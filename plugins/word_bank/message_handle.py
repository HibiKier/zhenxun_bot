from utils.message_builder import image, at
from ._rule import check
from .model import WordBank
from configs.path_config import DATA_PATH
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from utils.utils import get_message_at, get_message_img
from nonebot import on_message
from models.group_member_info import GroupInfoUser
from utils.utils import get_message_img_file, is_number
import re

__zx_plugin_name__ = "词库问答回复操作 [Hidden]"

data_dir = DATA_PATH / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)

message_handle = on_message(priority=6, block=True, rule=check)


@message_handle.handle()
async def _(event: GroupMessageEvent):
    msg = event.raw_message
    list_img = get_message_img_file(event.json())
    if list_img:
        for img_file in list_img:
            strinfo = re.compile(f"{img_file},subType=\d*]")
            msg = strinfo.sub(f'{img_file}]', msg)
    q = await WordBank.check(
        event.group_id, msg, event.is_tome()
    )
    await message_handle.send(await get_one_answer(event, q.format, q.answer))


# 处理单条回答
async def get_one_answer(event, format, _answer, all=1):
    path = data_dir / f"{event.group_id}"
    placeholder_list = (
        [
            (x.split("<_s>")[0], x.split("<_s>")[1])
            for x in format.split("<format>")[:-1]
        ]
        if format
        else []
    )
    answer = ""
    _a = _answer
    if not placeholder_list:
        answer = _a
        return answer
    else:
        for idx, placeholder in placeholder_list:
            if placeholder.endswith("jpg"):
                answer += _a[: _a.find(f"[__placeholder_{idx}]")] + image(
                    path / placeholder
                )
            else:
                if all == 1:
                    answer += _a[: _a.find(f"[__placeholder_{idx}]")] + at(placeholder)
                else:
                    q = await GroupInfoUser.get_member_info(
                        int(placeholder), event.group_id)
                    answer += _a[: _a.find(f"[__placeholder_{idx}]")] + "@" + q.user_name
            _a = _a[_a.find(f"[__placeholder_{idx}]") + len(f"[__placeholder_{idx}]"):]
    return answer + _a


# 处理单条问题
async def get_one_problem(event, problem):
    strinfo = re.compile(f",subType=\d")
    problem = strinfo.sub('', problem)
    _problem = problem
    _p = problem
    problem = ''
    for img in get_message_img(event.json()):
        _x = img.split("?")[0]
        r = re.search(rf"\[CQ:image,file=(.*),url={_x}.*?]", _p)
        if r:
            _problem = _problem.replace(
                rf",url={img}",
                f"",
            )
            problem += _p[: _p.find(f"[CQ:image,file={r.group(1)},url={img}]")] + image(img)
            _p = _p[
                 _p.find(f"[CQ:image,file={r.group(1)},url={img}]") + len(f"[CQ:image,file={r.group(1)},url={img}]"):]
    for at_ in get_message_at(event.json()):
        r = re.search(rf"\[CQ:at,qq={at_}]", problem)
        if r:
            q = await GroupInfoUser.get_member_info(
                int(at_), event.group_id)
            problem += _p[: _p.find(f"[CQ:at,qq={at_}]")] + "@" + q.user_name
            _p = _p[_p.find(f"[CQ:at,qq={at_}]") + len(f"[CQ:at,qq={at_}]"):]
    return _problem, problem + _p


# 显示单条数据库问题
async def get_one_image_problem(event, problem):
    path = data_dir / f"{event.group_id}" / "problem"
    placeholder_list = []
    idx = 0
    img_list = re.findall(rf"\[CQ:image,file=(.*?)]", problem)
    at_list = re.findall(rf"\[CQ:at,qq=(.*?)]", problem)
    if img_list:
        for img in img_list:
            problem = problem.replace(f'[CQ:image,file={img}]', f'[__placeholder_{idx}]', 1)
            placeholder_list.append([idx, img])
            idx += 1
    if at_list:
        for ats in at_list:
            problem = problem.replace(f'[CQ:at,qq={ats}]', f'[__placeholder_{idx}]', 1)
            placeholder_list.append([idx, ats])
            idx += 1
    _p = problem
    problem = ''
    if not placeholder_list:
        problem = _p
        return problem
    else:
        for idx, placeholder in placeholder_list:
            if is_number(placeholder):
                q = await GroupInfoUser.get_member_info(
                    int(placeholder), event.group_id)
                problem += _p[: _p.find(f"[__placeholder_{idx}]")] + "@" + q.user_name
            else:
                problem += _p[: _p.find(f"[__placeholder_{idx}]")] + image(
                    path / f"{placeholder}.jpg"
                )
            _p = _p[_p.find(f"[__placeholder_{idx}]") + len(f"[__placeholder_{idx}]"):]

    return problem + _p
