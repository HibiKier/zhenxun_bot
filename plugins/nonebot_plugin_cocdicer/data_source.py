# 参考[OlivaDiceDocs](https://oliva.dicer.wiki/userdoc)实现的nonebot2骰娘插件
import re
import random
from .messages import *


class Mylist(list):
    def next(self, index: int):
        if index < self.__len__()-1:
            return self[index+1]
        else:
            return ""


def help_message():
    return main_help_message


def dhr(t, o):
    if t == 0 and o == 0:
        return 100
    else:
        return t*10+o


def st():
    result = random.randint(1, 20)
    if result < 4:
        rstr = "右腿"
    elif result < 7:
        rstr = "左腿"
    elif result < 11:
        rstr = "腹部"
    elif result < 16:
        rstr = "胸部"
    elif result < 18:
        rstr = "右臂"
    elif result < 20:
        rstr = "左臂"
    elif result < 21:
        rstr = "头部"
    return "D20=%d：命中了%s" % (result, rstr)


def en(arg: str) -> str:
    try:
        arg = int(arg)
    except:
        return en_help_message
    check = random.randint(1, 100)
    if check > arg or check > 95:
        plus = random.randint(1, 10)
        r = "判定值%d，判定成功，技能成长%d+%d=%d" % (check, arg, plus, arg+plus)
        return r + "\n温馨提示：如果技能提高到90%或更高，增加2D6理智点数。"
    else:
        return "判定值%d，判定失败，技能无成长。" % check


class Dices(object):
    def __init__(self):
        self.dices = 1
        self.faces = 100
        self.a = False
        self.anum = 0
        self.h = False
        self.times = 1
        self.bp = 0
        self._bp_result = ""
        self._tens_place = None
        self._ones_place = None
        self._head = ""
        self._mid = ""
        self._end = ""
        self.result = 0
        self.a_check_mode = self.a_check
        self._a_check_result = ""
        self.ex_dice = None
        self.ex_dice_type = 1
        self._ex_result = ""

    def real_dice(self):
        if self.faces == 100:
            self._tens_place = random.randint(0, 9)
            self._ones_place = random.randint(0, 9)
            self.result += dhr(self._tens_place, self._ones_place)
            return dhr(self._tens_place, self._ones_place)
        else:
            rint = random.randint(1, self.faces)
            self.result += rint
        return rint

    def bp_dice(self):
        if not self.bp or self.faces != 100 or self.dices != 1:
            self._bp_result = ""
            return self._bp_result
        self._bp_result = " -> 十位：%d，个位：%d" % (
            self._tens_place, self._ones_place)
        bp = self.bp
        while bp > 0:
            bd = random.randint(0, 9)
            self._bp_result += "，奖励：%d" % bd
            if dhr(bd, self._ones_place) < dhr(self._tens_place, self._ones_place):
                self._tens_place = bd
                self.result = dhr(self._tens_place, self._ones_place)
            bp -= 1
        while bp < 0:
            bd = random.randint(0, 9)
            self._bp_result += "，惩罚：%d" % bd
            if dhr(bd,  self._ones_place) > dhr(self._tens_place, self._ones_place):
                self._tens_place = bd
                self.set_result()
            bp += 1
        return self._bp_result

    def a_check(self):
        if not (self.a and self.anum and self.faces == 100 and self.dices == 1):
            self._a_check_result = ""
            return self._a_check_result
        if self.result == 100:
            self._a_check_result = " 大失败！"
        elif self.anum < 50 and self.result > 95:
            self._a_check_result = "\n检定值%d %d>95 大失败！" % (
                self.anum, self.result)
        elif self.result == 1:
            self._a_check_result = " 大成功！"
        elif self.result <= self.anum // 5:
            self._a_check_result = "\n检定值%d %d≤%d 极难成功" % (
                self.anum, self.result, self.anum // 5)
        elif self.result <= self.anum // 2:
            self._a_check_result = "\n检定值%d %d≤%d 困难成功" % (
                self.anum, self.result, self.anum // 2)
        elif self.result <= self.anum:
            self._a_check_result = "\n检定值%d %d≤%d 成功" % (
                self.anum, self.result, self.anum)
        else:
            self._a_check_result = "\n检定值%d %d>%d 失败" % (
                self.anum, self.result, self.anum)
        return self._a_check_result

    def xdy(self):
        self.result = 0
        if self.dices == 1:
            self.real_dice()
            self.bp_dice()
            self.a_check()
            return ""
        else:
            dice_results = []
            for _ in range(self.dices):
                dice_result = self.real_dice()
                dice_results.append(str(dice_result))
            return "(%s)" % "+".join(dice_results)

    def _ex_handle(self):
        if not self.ex_dice:
            self._ex_result = ""
        elif type(self.ex_dice) == int:
            ex_result = self.ex_dice_type*self.ex_dice
            self._ex_result = "%s%s%d" % (str(
                self.result) if self.dices == 1 else "", "+" if self.ex_dice_type == 1 else "-", self.ex_dice)
            self.result += ex_result
        elif type(self.ex_dice) == Dices:
            self.ex_dice.roll
            ex_result = self.ex_dice_type*self.ex_dice.result
            self._ex_result = "%s%s%d" % (str(
                self.result) if self.dices == 1 else "", "+" if self.ex_dice_type == 1 else "-", self.ex_dice)
            self.result += ex_result
        return self._ex_result

    def roll(self):
        r = "%d次投掷：" % self.times
        if self.times != 1:
            r += "\n"
        for _ in range(self.times):
            xdyr = self.xdy()
            self._ex_handle()
            self._head = "%sD%d%s=" % (
                "" if self.dices == 1 else str(self.dices),
                self.faces,
                "" if not self.ex_dice else (
                    ("+" if self.ex_dice_type == 1 else "-") + str(self.ex_dice) if type(self.ex_dice) == int else (str(self.ex_dice.dices)+"D"+self.ex_dice.faces))
            )
            self._mid = "%s%s=" % (xdyr, self._ex_result)
            self._end = "%d%s%s" % (
                self.result, self._bp_result, self._a_check_result)
            r += "%s%s%s" % (self._head, self._mid if self.dices !=
                             1 or self.ex_dice else "", self._end)
            self.times -= 1
            if self.times:
                r += "\n"
        return r


def prework(args: list, start=0):
    for i in range(start, len(args), 1):
        if not re.search("\\d+", args[i]) and len(args[i]) > 1:
            p = args.pop(i)
            for j in list(p):
                args.insert(i, j)
                i += 1
            if prework(args, i):
                break
    return True


def rd(arg: str):
    try:
        h = False
        dices = Dices()
        args = re.split("(\\d+)", arg.lower())
        prework(args)
        args = Mylist(args)
        for i in range(len(args)):
            if args[i] == "a":
                dices.a = True
            elif args[i] == "#" and re.search("\\d+", args.next(i)):
                dices.times = int(args[i+1])
            elif args[i] == "b":
                dices.bp += 1
            elif args[i] == "p":
                dices.bp -= 1
            elif args[i] == "d" and re.search("\\d+", args.next(i)):
                dices.faces = int(args[i+1])
            elif args[i] == " " and re.search("\\d+", args.next(i)) and dices.a:
                dices.anum = int(args[i+1])
            elif args[i] == "h":
                h = True
            elif re.search("\\d+", args[i]):
                if args.next(i) == "d":
                    dices.dices = int(args[i])
                elif args[i-1] == " " and dices.a:
                    dices.anum = int(args[i])
            elif args[i] in ["-", "+"]:
                dices.ex_dice_type = (-1 if args[i] == "-" else 1)
                if args.next(i+1) == "d":
                    dices.ex_dice = Dices()
                    dices.ex_dice.dices = int(args.next(i))
                    dices.ex_dice.faces = int(args.next(i+2))
                elif args.next(i):
                    dices.ex_dice = int(args.next(i))
        if h:
            return [dices.roll()]
        return dices.roll()
    except:
        return r_help_message


if __name__ == "__main__":
    rd("2d100")
