# -*- coding: utf-8 -*-
"""
@Time ： 14/2/2023 2:59 pm
@Auth ： Jingrui Han
@File ：others.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""
import os
import numpy as np
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import torchvision.transforms as transforms
from PIL import Image
import torch
from time import time
import pickle
import yaml


def decode_yaml(yaml_path):
    with open(f"{yaml_path}", "r") as f:
        dict = yaml.safe_load(f)
    f.close()
    meta_params = dict["meta_params"]
    criteria_params = dict["criteria_params"]
    run_params = dict["running_params"]
    run_params["meta_params"] = meta_params
    run_params["criteria_params"] = criteria_params
    return meta_params, criteria_params, run_params


def create_folder(project):
    os.makedirs(project)
    print(f"{project} has been created!")
    os.makedirs(f"{project}/saved")
    print(f"saved folder has been created")
    os.makedirs(f"{project}/fail_test")
    print(f"fail_set folder has been created")


def torch_process(input_data):
    return torch.Tensor(input_data.copy().transpose(0, 3, 1, 2) / 255)


def keras_process(input_data):
    return input_data.copy() / 255


def compare_res(seeds_labels, mutation_preds, task_type, batch_size, k):
    """

    :param seeds_labels: an array [t1, t2, t3, t4......]
    :param mutation_preds: an array [[t11, t12, t13, t14....],
                                     [t21, t22, t23, t24....],
                                     [t31, t32, t33, t34....],
                                     ....]
    :param task_type:
    :return:
    """
    if task_type == "classification":
        # k = int(len(mutation_preds)/batch_size)
        comp_res = np.zeros((batch_size, k))
        mutation_preds = np.reshape(mutation_preds, (batch_size, k))
        for i in range(len(seeds_labels)):
            seed_label = seeds_labels[i]
            comp_res[i] = mutation_preds[i] == seed_label
        return comp_res


def convert_dimension(input_data, type, batch_size, k):
    """
    :param input_data: a list or dict
    :param type: reduce of increase
    :param batch_size: batch-size
    :return: an array
    """
    if type == "reduce":
        res = []
        for item in input_data:
            # temp_imgs = [item[key]['img']/255 for key in item]
            # 此处仅降维，不做任何别的处理
            temp_imgs = [item[key]["img"] for key in item]
            res += temp_imgs
        return np.array(res)
    elif type == "increase":
        # row_len = len(input_data)/batch_size
        row_len = k
        res = input_data.reshape(batch_size, row_len)
        return res


def decode_res(res, task_type):
    if task_type == "classification":
        temp_res = np.argmax(res, axis=1)
        # print(len(temp_res))
        return temp_res


def post_process(comp_array, final_array, mutation_preds, mutation_lst):
    # comp_array 对应的位置的数据进行储存，作为攻击成功样本
    # final_array 对应位置的数据进行储存，作为新seed
    # 分别返回需要储存的seeds信息和fail test信息
    # final矩阵中的T位置生成新seed
    # 预测矩阵中的F位置储存
    seed_save = []
    fail_smp_save = []
    indx_seed = np.where(final_array is True)
    indx_fail = np.where(comp_array is False)
    for i in range(len(indx_seed[0])):
        row, column = indx_seed[0][i], indx_seed[1][i]
        seed_save.append(mutation_lst[row][column])
    for i in range(len(indx_fail[0])):
        row, column = indx_fail[0][i], indx_fail[1][i]
        fail_smp_save.append(mutation_lst[row][column])
    return seed_save, fail_smp_save


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
    dataset = MyDataset(dir_path=dir_path, transform=transform())
    dataloader = DataLoader(dataset=dataset, batch_size=batch_size)
    return dataloader


class MyDataset(Dataset):
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


if __name__ == "__main__":
    pp = [[1], [2], [3], [4]]
    a1 = np.array([1, 2, 3, 4])
    rr = [[1, 2, 3], [2, 3, 3], [1, 3, 4], [4, 2, 4]]
    a2 = np.array(rr)
    print(np.where(a2 == 3))
