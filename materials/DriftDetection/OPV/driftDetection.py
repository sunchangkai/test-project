import os
import math
import numpy as np
import cv2
from scipy import stats
import time


def load_dataset(path):
    names = os.listdir(path)
    data_list = []
    for name in names:
        if name.endswith("png"):
            img_file = os.path.join(path, name)
            img = cv2.imread(img_file)
            height = img.shape[0]
            width = img.shape[1]
            if height != 48 or width != 48:
                img = cv2.resize(img, (48, 48))

            data = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            data_list.append(data)

    return np.array(data_list)


def batch_dict(data, resDict):
    row, column = data.shape
    for i in range(row):
        for j in range(column - 1):
            key = (data[i, j], data[i, j + 1])
            if key in resDict:
                num = resDict[key]
                resDict[key] = num + 1
            else:
                resDict[key] = 1
    # print(resDict)
    return resDict


def OPV_index(data_set, data_TPMDict):
    sumNum = sum(data_TPMDict.values())

    OPV_indexList = []
    for data in data_set:
        OPV_index = 0
        row, column = data.shape
        for i in range(row):
            for j in range(column - 1):
                key = (data[i, j], data[i, j + 1])
                OPV_index -= math.log(data_TPMDict[key] / sumNum)

        OPV_indexList.append(OPV_index)

    OPV_indexArray = np.array(OPV_indexList)

    return OPV_indexArray


def TPM(data_set):
    resDict = {}
    for data in data_set:
        resDict = batch_dict(data, resDict)
    return resDict


# Student's t-test
def t_test(ref_OPV_indexArray, test_OPV_indexArray):
    stat, p = stats.ttest_ind(ref_OPV_indexArray, test_OPV_indexArray)

    if p > 0.05:
        return 0
    else:
        return 1


def OPV_detection(ref_path, test_path):
    ref_set = load_dataset(ref_path)
    test_set = load_dataset(test_path)

    print(len(ref_set), len(test_set))
    s_time = time.time()
    ref_TPMDict = TPM(ref_set)
    test_TPMDict = TPM(test_set)

    ref_OPV_indexArray = OPV_index(ref_set, ref_TPMDict)
    test_OPV_indexArray = OPV_index(test_set, test_TPMDict)
    label = t_test(ref_OPV_indexArray, test_OPV_indexArray)
    # print(len(test_OPV_indexArray), len(ref_OPV_indexArray))
    return label, time.time() - s_time
