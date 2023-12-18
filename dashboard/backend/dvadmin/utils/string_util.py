# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/8/21 021 9:48
@Remark:
"""
import hashlib
import random

CHAR_SET = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
)


def random_str(number=16):
    """
    returns a random string of a specific length (non hexadecimal)
    :return:
    """
    result = ""
    for i in range(0, number):
        inx = random.randint(0, len(CHAR_SET) - 1)
        result += CHAR_SET[inx]
    return result


def has_md5(str, salt="123456"):
    """
    md5
    :param str:
    :param salt:
    :return:
    """

    str = str + salt
    md = hashlib.md5()
    md.update(str.encode())
    res = md.hexdigest()
    return res
