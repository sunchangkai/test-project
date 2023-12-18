import torchvision.transforms as transforms
import torch
import os

# import cv2
from torch.utils.data.dataset import Dataset
from PIL import Image
from torch.utils.data import DataLoader
import pickle
from time import time

# import numpy as np


def transform(mean=None, std=None, size: tuple = (48, 48)):
    if std is None:
        std = [0.5, 0.5, 0.5]
    if mean is None:
        mean = [0.5, 0.5, 0.5]
    # normalize = transforms.Normalize(mean=mean, std=std)
    return transforms.Compose(
        [
            transforms.Resize(size),
            transforms.ToTensor(),
            # normalize
        ]
    )


def build_dataset(dir_path: str, batch_size=6):
    dataset = Mydataset(dir_path=dir_path, transform=transform())
    dataloader = DataLoader(dataset=dataset, batch_size=batch_size)
    return dataloader


class Mydataset(Dataset):
    def __init__(self, dir_path, transform):
        self.dir_path = dir_path
        o_paths = os.listdir(self.dir_path)
        self.paths = []
        for path in o_paths:
            if path == ".DS_Store":
                continue
            temp_path = f"{dir_path}/{path}"
            self.paths.append(temp_path)
        self.transform = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, index):
        temp_path = self.paths[index]
        img = Image.open(temp_path)
        img = self.transform(img)
        return img


def save_pickle(dict, root_dir):
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    name = time()
    with open(f"{root_dir}/{name}.pkl", "wb") as f:
        pickle.dump(dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    return f"{name}.pkl"


def read_pickle(root_dir, name_lst):
    if not os.path.exists(f"{root_dir}"):
        raise NameError(f"{root_dir} is not existed")
    for item in name_lst:
        if item.endswith("pkl"):
            with open(f"{root_dir}/{item}", "rb") as f:
                red = pickle.load(f)
                f.close()
            yield red["coverage_table"]


def merge_pickle(root_dir, name_lst):
    pre = None
    iteror = read_pickle(root_dir, name_lst)
    while 1:
        if not pre:
            pre = iteror.__next__()
        else:
            try:
                current = iteror.__next__()
            except Exception:
                break
            if not current:
                break
            for key in current.keys():
                pre[key] = (pre[key] + current[key]) > 0

    return pre


def scale(m):
    """
    apply minmax normalization
    :param m: a 3 dimension array or tensor (batch, c, v)
    :return:
    """
    # return (m - m.min()) / (m.max() - m.min())
    min_m = torch.min(m, dim=2).values  # (batch, c) 已被压平，沿第三个（dim=2）维度求最小
    max_m = torch.max(m, dim=2).values  # (batch, c) 已被压平，沿第三个（dim=2）维度求最大
    max_min = max_m - min_m + 1 / 100000
    res = (m - min_m[:, :, None]) / max_min[:, :, None]  # 输出为（batch， c， x）
    return res
