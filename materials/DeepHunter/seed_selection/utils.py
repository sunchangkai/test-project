import os
import numpy as np
import cv2
from time import time
from scipy.special import softmax
from lib.logger import Logger


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


class seed(object):
    def __init__(self, path, init_path, ref_path, m_time, p_min, r, state, label):
        self.m_time = m_time
        self.p_min = p_min
        self.p = 1
        self.path = path
        self.r = r
        self.state = state
        self.init_path = init_path
        self.ref_path = ref_path
        self.label = label

    def get_p(self):
        if self.m_time < (1 - self.p_min) * self.r:
            self.p = 1 - (self.m_time / self.r)
            return self.p
        else:
            self.p = self.p_min
            return self.p


class seedsQueue(object):
    def __init__(self, seed_paths, p_min, r, project):
        self.seeds_pro = []
        self.seeds_m_time = []
        self.seeds_states = []
        self.p_min = p_min
        self.r = r
        self.project = project
        self.length = 0
        for path in seed_paths:
            label = get_label(path)
            with open(f"{self.project}/seed_info.txt", "a") as f:
                ss = f"path:{path},p_min:{self.p_min},r:{self.r},init_path:{path},ref_path:{path},label:{label}\n"
                f.write(ss)
                f.close()
            self.length += 1
            self.seeds_pro.append(1)
            self.seeds_m_time.append(0)
            self.seeds_states.append(0)
            # self.seeds.append(seed(path=path, m_time=0, p_min=self.p_min, r=self.r, state=0,
            #                        init_path=path, ref_path=path, label=label))
        self.logger = Logger(log_name=project, log_path=f"{project}/Mylog.log")

    def get_seed(self, num: int):
        seeds_p = self.get_seeds_p()
        indxs = [i for i in range(self.get_length())]
        s_indx = np.random.choice(indxs, num, p=seeds_p, replace=False)
        temp_seeds = []
        s_indx = sorted(s_indx)
        with open(f"{self.project}/seed_info.txt", "r") as f:
            for i in range(s_indx[-1] + 1):
                s = f.readline()
                if i in s_indx:
                    temp_dict = self.decode(s)
                    temp_seeds.append(
                        seed(
                            path=temp_dict["path"],
                            init_path=temp_dict["init_path"],
                            ref_path=temp_dict["ref_path"],
                            label=int(temp_dict["label"]),
                            m_time=self.seeds_m_time[i],
                            p_min=self.p_min,
                            state=self.seeds_states[i],
                            r=self.r,
                        )
                    )
        # temp_seeds = self.seeds[s_indx[0]]
        return s_indx, temp_seeds

    def add_seed(self, path, state, init_seed, ref_path, label):
        # new_seed = seed(path=path, m_time=0, p_min=self.p_min, r=self.r, state=state,
        #                 init_path=init_seed, ref_path=ref_path, label=label)
        with open(f"{self.project}/seed_info.txt", "a") as f:
            ss = f"path:{path},p_min:{self.p_min},r:{self.r},init_path:{init_seed},ref_path:{ref_path},label:{label}\n"
            f.write(ss)
            f.close()
        self.seeds_pro.append(1)
        self.seeds_m_time.append(0)
        self.seeds_states.append(state)
        self.logger.add_log(
            s=f"add new seed successfully, "
            f"current seed queue length: {self.get_length()}, new path: {path}, "
            f"init path: {init_seed}, ref_path: {ref_path}, label: {label}, state: {state}"
        )
        # print(f"add new seed successfully, "
        #       f"current seed queue length: {self.get_length()}, new path: {path}"
        #       f"init path: {init_seed}, ref_path: {ref_path}, label: {label}, state: {state}")

    def update_seed(self, index, m_time):
        # temp_seed_pro = self.seeds_pro[index]
        self.seeds_m_time[index] += 1
        self.seeds_pro[index] = self.cal_p(m_time=self.seeds_m_time[index])
        self.logger.add_log(
            s=f"update seed info successfully, current p is {self.seeds_pro[index]}"
        )
        # print(f'update seed info successfully, current p is {temp_seed.p}')

    # def get_detail(self):
    #     res = {}
    #     c = 0
    #     for seed in self.seeds_pro:
    #         temp = {
    #             'path': seed.path,
    #             'p': seed.p,
    #             'mutation times': seed.m_time,
    #             'state': seed.state,
    #             'init_path': seed.init_path,
    #             'ref_path': seed.ref_path,
    #             'label': seed.label
    #         }
    #         c += 1
    #         res[c] = temp
    #     return res

    def get_length(self):
        if (len(self.seeds_states) == len(self.seeds_pro)) and (
            len(self.seeds_pro) == len(self.seeds_m_time)
        ):
            return len(self.seeds_states)
        else:
            raise Exception(
                "internal error the length of seed states ,"
                " seeds probability and seed m_time are not same!"
            )

    def get_seeds_p(self):
        temp_res = softmax(self.seeds_pro, axis=0)
        return temp_res

    def cal_p(self, m_time):
        if m_time < (1 - self.p_min) * self.r:
            p = 1 - (m_time / self.r)
            return p
        else:
            p = self.p_min
            return p

    def decode(self, s):
        res = {}
        s_lst = s.strip("\n").split(",")
        for item in s_lst:
            temp_lst = item.split(":")
            res[temp_lst[0]] = temp_lst[1]
        return res


if __name__ == "__main__":
    img_dir = "../data/fewer"
    seed_paths = scan_imgs(img_dir)
    seed_queue = seedsQueue(seed_paths=seed_paths, p_min=0.7, r=10, project="../test")
    seeds = seed_queue.get_seed(num=3)
    print(seeds)
