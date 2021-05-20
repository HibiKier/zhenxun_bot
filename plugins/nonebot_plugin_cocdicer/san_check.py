from .data_source import Dices
from .messages import sc_help_message

import re


def number_or_dice(arg: str):
    if "d" in arg:
        d = Dices()
        if dices := re.search(r"\d+d", arg):
            d.dices = int(dices.group()[:-1])
        if faces := re.search(r"d\d+", arg):
            d.faces = int(faces.group()[1:])
        d.roll()
        return d
    else:
        return int(arg)


def sc(arg: str) -> str:
    a_num = re.search(r" \d+", arg)
    success = re.search(r"\d*d\d+|\d+", arg)
    failure = re.search(r"[\/]+(\d*d\d+|\d+)", arg)
    if not (a_num and success and failure):
        return sc_help_message
    check_dice = Dices()
    check_dice.a = True
    check_dice.anum = int(a_num.group()[1:])
    success = number_or_dice(success.group())
    failure = number_or_dice(failure.group()[1:])
    r = "San Check" + check_dice.roll()[4:]
    result = success if check_dice.result <= check_dice.anum else failure
    r += "\n理智降低了"
    if type(result) == int:
        r += "%d点" % result
    else:
        r = r + result._head + str(result.result)
    return r
