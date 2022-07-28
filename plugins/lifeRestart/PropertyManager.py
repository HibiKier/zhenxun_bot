from typing import Dict, Set

sum_data = {
    "CHR": [
        {"min": 0, "judge": "地狱", "grade": 0},
        {"min": 1, "judge": "折磨", "grade": 0},
        {"min": 2, "judge": "不佳", "grade": 0},
        {"min": 4, "judge": "普通", "grade": 0},
        {"min": 7, "judge": "优秀", "grade": 1},
        {"min": 9, "judge": "罕见", "grade": 2},
        {"min": 11, "judge": "逆天", "grade": 3},
    ],
    "MNY": [
        {"min": 0, "judge": "地狱", "grade": 0},
        {"min": 1, "judge": "折磨", "grade": 0},
        {"min": 2, "judge": "不佳", "grade": 0},
        {"min": 4, "judge": "普通", "grade": 0},
        {"min": 7, "judge": "优秀", "grade": 1},
        {"min": 9, "judge": "罕见", "grade": 2},
        {"min": 11, "judge": "逆天", "grade": 3},
    ],
    "SPR": [
        {"min": 0, "judge": "地狱", "grade": 0},
        {"min": 1, "judge": "折磨", "grade": 0},
        {"min": 2, "judge": "不幸", "grade": 0},
        {"min": 4, "judge": "普通", "grade": 0},
        {"min": 7, "judge": "幸福", "grade": 1},
        {"min": 9, "judge": "极乐", "grade": 2},
        {"min": 11, "judge": "天命", "grade": 3},
    ],
    "INT": [
        {"min": 0, "judge": "地狱", "grade": 0},
        {"min": 1, "judge": "折磨", "grade": 0},
        {"min": 2, "judge": "不佳", "grade": 0},
        {"min": 4, "judge": "普通", "grade": 0},
        {"min": 7, "judge": "优秀", "grade": 1},
        {"min": 9, "judge": "罕见", "grade": 2},
        {"min": 11, "judge": "逆天", "grade": 3},
        {"min": 21, "judge": "识海", "grade": 3},
        {"min": 131, "judge": "元神", "grade": 3},
        {"min": 501, "judge": "仙魂", "grade": 3},
    ],
    "STR": [
        {"min": 0, "judge": "地狱", "grade": 0},
        {"min": 1, "judge": "折磨", "grade": 0},
        {"min": 2, "judge": "不佳", "grade": 0},
        {"min": 4, "judge": "普通", "grade": 0},
        {"min": 7, "judge": "优秀", "grade": 1},
        {"min": 9, "judge": "罕见", "grade": 2},
        {"min": 11, "judge": "逆天", "grade": 3},
        {"min": 21, "judge": "凝气", "grade": 3},
        {"min": 101, "judge": "筑基", "grade": 3},
        {"min": 401, "judge": "金丹", "grade": 3},
        {"min": 1001, "judge": "元婴", "grade": 3},
        {"min": 2001, "judge": "仙体", "grade": 3},
    ],
    "AGE": [
        {"min": 0, "judge": "胎死腹中", "grade": 0},
        {"min": 1, "judge": "早夭", "grade": 0},
        {"min": 10, "judge": "少年", "grade": 0},
        {"min": 18, "judge": "盛年", "grade": 0},
        {"min": 40, "judge": "中年", "grade": 0},
        {"min": 60, "judge": "花甲", "grade": 1},
        {"min": 70, "judge": "古稀", "grade": 1},
        {"min": 80, "judge": "杖朝", "grade": 2},
        {"min": 90, "judge": "南山", "grade": 2},
        {"min": 95, "judge": "不老", "grade": 3},
        {"min": 100, "judge": "修仙", "grade": 3},
        {"min": 500, "judge": "仙寿", "grade": 3},
    ],
    "SUM": [
        {"min": 0, "judge": "地狱", "grade": 0},
        {"min": 41, "judge": "折磨", "grade": 0},
        {"min": 50, "judge": "不佳", "grade": 0},
        {"min": 60, "judge": "普通", "grade": 0},
        {"min": 80, "judge": "优秀", "grade": 1},
        {"min": 100, "judge": "罕见", "grade": 2},
        {"min": 110, "judge": "逆天", "grade": 3},
        {"min": 120, "judge": "传说", "grade": 3},
    ]
}


class PropertyManager:
    def __init__(self, base):
        self._base = base
        self.CHR = 0 # 颜值 charm CHR
        self.INT = 0 # 智力 intelligence INT
        self.STR = 0 # 体质 strength STR
        self.MNY = 0 # 家境 money MNY
        self.SPR = 5 # 快乐 spirit SPR

        self.AGE = -1
        self.LIF = 1 # hp
        
        self.total = 20
    
    @property
    def TLT(self) -> Set[int]: # 天赋 talent TLT
        return self._base.talent.triggered

    @property
    def EVT(self) -> Set[int]:
        return self._base.event.triggered

    def apply(self, effect: Dict[str, int]):
        for key in effect:
            setattr(self, key, getattr(self, key) + effect[key])
            
    def gensummary(self):
        summary = '==人生总结==\n\n'

        judge = '地狱'
        for res in sum_data['CHR']:
            if self.CHR >= res["min"]:
                judge = res["judge"]
            else:
                break
        summary = summary + "颜值:  " + str(self.CHR)+"  "+judge+"\n"

        judge = '地狱'
        for res in sum_data['INT']:
            if self.INT >= res["min"]:
                judge = res["judge"]
            else:
                break
        summary = summary + "智力:  " + str(self.INT)+"  "+judge+"\n"

        judge = '地狱'
        for res in sum_data['STR']:
            if self.STR >= res["min"]:
                judge = res["judge"]
            else:
                break
        summary = summary + "体质:  " + str(self.STR)+"  "+judge+"\n"

        judge = '地狱'
        for res in sum_data['MNY']:
            if self.MNY >= res["min"]:
                judge = res["judge"]
            else:
                break
        summary = summary + "家境:  " + str(self.MNY)+"  "+judge+"\n"

        judge = '地狱'
        for res in sum_data['SPR']:
            if self.SPR >= res["min"]:
                judge = res["judge"]
            else:
                break
        summary = summary + "快乐:  " + str(self.SPR)+"  "+judge+"\n"

        judge = '胎死腹中'
        for res in sum_data['AGE']:
            if self.AGE >= res["min"]:
                judge = res["judge"]
            else:
                break
        summary = summary + "享年:  " + str(self.AGE)+"  "+judge+"\n"

        summary = summary + '\n'

        judge = '地狱'
        sum = int((self.CHR+self.INT+self.STR+self.MNY+self.SPR)*2+self.AGE/2)
        for res in sum_data['SUM']:
            if sum >= res["min"]:
                judge = res["judge"]
            else:
                break
        summary = summary + "总评:  " + str(sum) + "  " + judge + "\n"

        return summary
