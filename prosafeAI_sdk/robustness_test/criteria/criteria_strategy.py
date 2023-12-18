# -*- coding: utf-8 -*-
"""
@Time ： 14/2/2023 3:09 pm
@Auth ： Jingrui Han
@File ：CriteriaStrategy.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""
import torch

# from prosafeAI_sdk.robustness_test.utils.others import build_dataset
from prosafeAI_sdk.robustness_test.criteria.KMNC import CalKMNCKeras, CalKMNCTorch
from prosafeAI_sdk.robustness_test.criteria.NC import CalNCTorch, CalNCKeras
from prosafeAI_sdk.robustness_test.criteria.TopK import CalTopKTorch, CalTopKKeras
from prosafeAI_sdk.robustness_test.criteria.NS import CalNSTorch, CalNSKeras
from prosafeAI_sdk.robustness_test.model.model import MyModel
import numpy as np


class CriteriaStrategy(object):
    def __init__(self, criteria, model: MyModel, params, dl_frame, batch_size, device):
        self.criteria = criteria[0]
        self.model = model.model
        self.params = params
        self.dl_frame = dl_frame
        self.cal_funcs = {
            "NC": {"torch": CalNCTorch, "keras": CalNCKeras},
            "KMNC": {"torch": CalKMNCTorch, "keras": CalKMNCKeras},
            "TopK": {"torch": CalTopKTorch, "keras": CalTopKKeras},
            "NeuronSensitivity": {"torch": CalNSTorch, "keras": CalNSKeras},
        }
        self.batch_size = batch_size
        self.device = device

    def calculate(self):
        self.params[self.criteria]["model"] = self.model
        # tmp_cal_fn = self.cal_funcs[self.criteria][self.dl_frame](**self.params[self.criteria])
        if self.criteria in ["NC", "TopK"]:
            # do not make data preparation
            if self.dl_frame in ["torch"]:
                tmp_cal_fn = self.cal_funcs[self.criteria][self.dl_frame](
                    **self.params[self.criteria]
                )
                res_ori = tmp_cal_fn.run_once(self.original_seeds.to(self.device))
                tmp_cal_fn = self.cal_funcs[self.criteria][self.dl_frame](
                    **self.params[self.criteria]
                )
                res_mut = tmp_cal_fn.run_once(self.mutators.to(self.device))
            elif self.dl_frame in ["keras"]:
                tmp_cal_fn = self.cal_funcs[self.criteria][self.dl_frame](
                    **self.params[self.criteria]
                )
                res_ori = tmp_cal_fn.run_once(self.original_seeds)
                tmp_cal_fn = self.cal_funcs[self.criteria][self.dl_frame](
                    **self.params[self.criteria]
                )
                res_mut = tmp_cal_fn.run_once(self.mutators)
        elif self.criteria in ["KMNC"]:
            # train_dataset = load_dataset_kmnc(self.params[self.criteria]['train_data_path'])
            # self.params[self.criteria]['train_dataset'] = train_dataset
            tmp_cal_fn = self.cal_funcs[self.criteria][self.dl_frame](
                **self.params[self.criteria]
            )
            res_ori = []
            res_mut = []
            # calculate original
            for o_item in self.original_seeds:
                if self.dl_frame in ["onnx", "keras"]:
                    o_item = np.expand_dims(o_item, axis=0)
                elif self.dl_frame in ["torch"]:
                    o_item = o_item.unsqueeze(0)
                tmp_res = tmp_cal_fn.run_once(o_item)
                res_ori.append(tmp_res)
            # calculate mutation images
            for m_item in self.mutators:
                if self.dl_frame in ["onnx", "keras"]:
                    m_item = np.expand_dims(m_item, axis=0)
                elif self.dl_frame in ["torch"]:
                    m_item = m_item.unsqueeze(0)
                tmp_res = tmp_cal_fn.run_once(m_item)
                res_mut.append(tmp_res)
            # convert to np
            res_ori, res_mut = np.array(res_ori), np.array(res_mut)

        elif self.criteria in ["NeuronSensitivity"]:
            # do data preparation
            tmp_cal_fn = self.cal_funcs[self.criteria][self.dl_frame](
                **self.params[self.criteria]
            )
            if self.dl_frame in ["keras", "onnx"]:
                # data preparation end
                tmp_o_data = []
                for i in range(len(self.original_seeds)):
                    for j in range(int(len(self.mutators) / self.batch_size)):
                        tmp_o_data.append(self.original_seeds[i])
                tmp_o_data = np.array(tmp_o_data)
                res_mut = tmp_cal_fn.run_once(tmp_o_data, self.mutators)
                res_ori = None
            elif self.dl_frame in ["torch"]:
                # 格式转换 如何tensor-》tensor
                k = int(len(self.mutators) / self.batch_size)
                tmp_o_data = torch.zeros_like(self.mutators)
                for i in range(self.batch_size):
                    for j in range(k):
                        tmp_o_data[(i * k) + j] = self.original_seeds[i]
                res_mut = tmp_cal_fn.run_once(tmp_o_data, self.mutators)
                res_ori = None
        return res_ori, res_mut

    def justify_res(self):
        comp_res = np.zeros_like(self.res_m)

        if self.criteria in ["NC", "TopK", "KMNC"]:
            for i in range(len(self.res_o)):
                ttt = self.res_o[i] < self.res_m[i]
                comp_res[i] = ttt

        elif self.criteria in ["NS"]:
            for i in range(len(self.original_seeds)):
                comp_res[i] = self.res_m[i] > self.params["e"]

        return comp_res

    def test_once(self, original_seeds, mutators):
        self.original_seeds, self.mutators = original_seeds, mutators
        # calculate the mutation images
        self.res_o, self.res_m = self.calculate()
        # calculate the original images
        # reshape the res_m to original shape
        k = int(len(self.res_m) / self.batch_size)
        self.res_m = self.res_m.reshape(self.batch_size, k)
        # justify_res
        res = self.justify_res()
        # return a numpy array:
        # [[0, 0, 0, 0],
        #  [1, 0, 1, 1],
        #  [1, 0, 1, 1],
        #  ]
        # 大的用1， 小的用0，外部和对错矩阵进行或运算合并
        return res
