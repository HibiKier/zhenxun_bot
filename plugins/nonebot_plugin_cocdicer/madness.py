import random

from .messages import temporary_madness, madness_end, phobias, manias


def ti():
    i = random.randint(1, 10)
    r = "临时疯狂判定1D10=%d\n" % i
    r += temporary_madness[i-1]
    if i == 9:
        j = random.randint(1, 100)
        r += "\n恐惧症状为：\n"
        r += phobias[j-1]
    elif i == 10:
        j = random.randint(1, 100)
        r += "\n狂躁症状为：\n"
        r += manias[j-1]
    r += "\n该症状将会持续1D10=%d" % random.randint(1, 10)
    return r


def li():
    i = random.randint(1, 10)
    r = "总结疯狂判定1D10=%d\n" % i
    r += madness_end[i-1]
    if i in [2, 3, 6, 9, 10]:
        r += "\n调查员将在1D10=%d小时后醒来" % random.randint(1, 10)
    if i == 9:
        j = random.randint(1, 100)
        r += "\n恐惧症状为：\n"
        r += phobias[j-1]
    elif i == 10:
        j = random.randint(1, 100)
        r += "\n狂躁症状为：\n"
        r += manias[j-1]
    return r
