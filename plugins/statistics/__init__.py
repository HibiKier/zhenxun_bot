from configs.path_config import DATA_PATH
import nonebot
import os
try:
    import ujson as json
except ModuleNotFoundError:
    import json

nonebot.load_plugins("plugins/statistics")

old_file1 = DATA_PATH / "_prefix_count.json"
old_file2 = DATA_PATH / "_prefix_user_count.json"
new_path = DATA_PATH / "statistics"
new_path.mkdir(parents=True, exist_ok=True)
if old_file1.exists():
    os.rename(old_file1, new_path / "_prefix_count.json")
if old_file2.exists():
    os.rename(old_file2, new_path / "_prefix_user_count.json")


# 修改旧数据

statistics_group_file = DATA_PATH / "statistics" / "_prefix_count.json"
statistics_user_file = DATA_PATH / "statistics" / "_prefix_user_count.json"

for file in [statistics_group_file, statistics_user_file]:
    if file.exists():
        with open(file, "r", encoding="utf8") as f:
            data = json.load(f)
            if not (statistics_group_file.parent / f"{file}.bak").exists():
                with open(f"{file}.bak", "w", encoding="utf8") as wf:
                    json.dump(data, wf, ensure_ascii=False, indent=4)
            for x in ["total_statistics", "day_statistics"]:
                for key in data[x].keys():
                    num = 0
                    if data[x][key].get("ai") is not None:
                        if data[x][key].get("Ai") is not None:
                            data[x][key]["Ai"] += data[x][key]["ai"]
                        else:
                            data[x][key]["Ai"] = data[x][key]["ai"]
                        del data[x][key]["ai"]
                    if data[x][key].get("抽卡") is not None:
                        if data[x][key].get("游戏抽卡") is not None:
                            data[x][key]["游戏抽卡"] += data[x][key]["抽卡"]
                        else:
                            data[x][key]["游戏抽卡"] = data[x][key]["抽卡"]
                        del data[x][key]["抽卡"]
                    if data[x][key].get("我的道具") is not None:
                        num += data[x][key]["我的道具"]
                        del data[x][key]["我的道具"]
                    if data[x][key].get("使用道具") is not None:
                        num += data[x][key]["使用道具"]
                        del data[x][key]["使用道具"]
                    if data[x][key].get("我的金币") is not None:
                        num += data[x][key]["我的金币"]
                        del data[x][key]["我的金币"]
                    if data[x][key].get("购买") is not None:
                        num += data[x][key]["购买"]
                        del data[x][key]["购买"]
                    if data[x][key].get("商店") is not None:
                        data[x][key]["商店"] += num
                    else:
                        data[x][key]["商店"] = num
            for x in ["week_statistics", "month_statistics"]:
                for key in data[x].keys():
                    if key == "total":
                        if data[x][key].get("ai") is not None:
                            if data[x][key].get("Ai") is not None:
                                data[x][key]["Ai"] += data[x][key]["ai"]
                            else:
                                data[x][key]["Ai"] = data[x][key]["ai"]
                            del data[x][key]["ai"]
                        if data[x][key].get("抽卡") is not None:
                            if data[x][key].get("游戏抽卡") is not None:
                                data[x][key]["游戏抽卡"] += data[x][key]["抽卡"]
                            else:
                                data[x][key]["游戏抽卡"] = data[x][key]["抽卡"]
                            del data[x][key]["抽卡"]
                        if data[x][key].get("我的道具") is not None:
                            num += data[x][key]["我的道具"]
                            del data[x][key]["我的道具"]
                        if data[x][key].get("使用道具") is not None:
                            num += data[x][key]["使用道具"]
                            del data[x][key]["使用道具"]
                        if data[x][key].get("我的金币") is not None:
                            num += data[x][key]["我的金币"]
                            del data[x][key]["我的金币"]
                        if data[x][key].get("购买") is not None:
                            num += data[x][key]["购买"]
                            del data[x][key]["购买"]
                        if data[x][key].get("商店") is not None:
                            data[x][key]["商店"] += num
                        else:
                            data[x][key]["商店"] = num
                    else:
                        for day in data[x][key].keys():
                            num = 0
                            if data[x][key][day].get("ai") is not None:
                                if data[x][key][day].get("Ai") is not None:
                                    data[x][key][day]["Ai"] += data[x][key][day]["ai"]
                                else:
                                    data[x][key][day]["Ai"] = data[x][key][day]["ai"]
                                del data[x][key][day]["ai"]
                            if data[x][key][day].get("抽卡") is not None:
                                if data[x][key][day].get("游戏抽卡") is not None:
                                    data[x][key][day]["游戏抽卡"] += data[x][key][day]["抽卡"]
                                else:
                                    data[x][key][day]["游戏抽卡"] = data[x][key][day]["抽卡"]
                                del data[x][key][day]["抽卡"]
                            if data[x][key][day].get("我的道具") is not None:
                                num += data[x][key][day]["我的道具"]
                                del data[x][key][day]["我的道具"]
                            if data[x][key][day].get("使用道具") is not None:
                                num += data[x][key][day]["使用道具"]
                                del data[x][key][day]["使用道具"]
                            if data[x][key][day].get("我的金币") is not None:
                                num += data[x][key][day]["我的金币"]
                                del data[x][key][day]["我的金币"]
                            if data[x][key][day].get("购买") is not None:
                                num += data[x][key][day]["购买"]
                                del data[x][key][day]["购买"]
                            if data[x][key][day].get("商店") is not None:
                                data[x][key][day]["商店"] += num
                            else:
                                data[x][key][day]["商店"] = num
        with open(file, "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
