import numpy as np
import os


def preprocessing(img: np.ndarray):
    """
    please modify it depends
    :param img:
    :return:
    """
    img = img / 255
    return img


def scan_imgs(dir):
    "this function could be modified to fit the different data structure"
    res = []
    for cls in os.listdir(dir):
        if cls == ".DS_Store":
            continue
        for item in os.listdir(f"{dir}/{cls}"):
            if item.endswith(".png"):
                res.append(f"{dir}/{cls}/{item}")
    return res


def get_label(path):
    s = path.split("/")[-2]
    return int(s)
