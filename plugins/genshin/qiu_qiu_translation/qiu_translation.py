import json
import os

FILE_PATH = os.path.dirname(__file__)

QIU_QIU_WORD = {}
QIU_QIU_PHRASE = {}

with open(
    os.path.join(FILE_PATH, "qiu_qiu_dictionary.json"), "r", encoding="UTF-8"
) as f:
    data = json.load(f)
    QIU_QIU_WORD = data["word"]
    QIU_QIU_PHRASE = data["phrase"]


def compare_words(word):
    # 比对word库是否有匹配的单词，有的话返回翻译，没有返回原词
    if word in QIU_QIU_WORD:
        return QIU_QIU_WORD[word]

    return word


def compare_phrase(phrase):
    # 比对phrase库是否有匹配的单词，有的话返回翻译，没有的话匹配word库，都没有返回原词
    if phrase in QIU_QIU_PHRASE:
        return QIU_QIU_PHRASE[phrase]
    if phrase in QIU_QIU_WORD:
        return QIU_QIU_WORD[phrase]

    return phrase


def qiu_qiu_word_translation(txt: str):
    # 对语句按空格分隔替换单词翻译
    txt_list = txt.split(" ")
    mes = "你查询的的丘丘语意思为:\n"

    for word in txt_list:
        tra_word = compare_words(word)

        if tra_word == word:
            # 如果是原词表示没有翻译，前后加空格接回语句里
            if not mes[-1] == " ":
                mes += " "
            mes += tra_word
            mes += " "
        else:
            mes += tra_word
    mes += "\n"
    return mes


def qiu_qiu_phrase_translation(phrase):
    # 语句翻译，先看phrase库是不是有匹配的语句
    # 没有的话把单词拆开返回单词的意思
    tra_phrase = compare_phrase(phrase)
    if tra_phrase != phrase:
        return f"\n翻译丘丘语意思为:\n【{tra_phrase}】\n"

    txt_list = phrase.split(" ")
    mes = "没有查到这句丘丘语,以下是单词的翻译\n"
    for word in txt_list:
        if word == " ":
            continue
        tra_word = compare_phrase(word)
        if tra_word == word:
            mes += f"{word} : 没有这个词的翻译\n"
        else:
            mes += f"{word} : {tra_word}\n"

    return mes
