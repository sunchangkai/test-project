# -*- coding: utf-8 -*-
"""
@Time ： 20/2/2023 1:57 pm
@Auth ： Jingrui Han
@File ：NC.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""

from collections import defaultdict
from keras import Model
from prosafeAI_sdk.robustness_test.utils.others import (
    build_dataset,
    save_pickle,
    merge_pickle,
    scale,
)
import torch
import numpy as np
from torch.utils.data import DataLoader
from tqdm import tqdm
import pickle


class CalNCTorch(object):
    def __init__(
        self,
        model: torch.nn.Module,
        model_name: str,
        threshold: float = 0.75,
        act_fn=None,
    ):
        if act_fn is None:
            self.act_fn = ["relu"]
        else:
            self.act_fn = act_fn
        self.model = model
        self.model.eval()
        self.threshold = threshold
        self.model_dict = self.get_model_dict(self.model)
        self.output_nc_table = {}
        self.stat_info = {}
        self.merge_flag = False
        self.model_name = model_name
        self.sub_file_lst = []
        self.total_info = {}
        self.c = 0

    def get_model_dict(self, model: torch.nn.Module):
        """
        usded to get the output from model in each target layer
        :param model: model
        :return:
        """
        self.temp_dict = {}
        neurons = set()
        # self.c = 1
        for name in dict(model.named_modules()):
            # print(name)
            temp_name = name.split(".")[-1]
            if temp_name in self.act_fn:
                neurons.add(name)

        def set_table(name):
            def hook(model, input, output):
                if name in self.temp_dict:
                    temp_name = name + self.c * ".1"
                    self.c += 1
                    self.temp_dict[temp_name] = output
                else:
                    self.temp_dict[name] = output
                    self.c = 1

            return hook

        for name, layer in model.named_modules():
            if name in neurons:
                # print(name)
                layer.register_forward_hook(set_table(name))
        return self.temp_dict

    def init_cover_dict(self):
        activate_table = defaultdict()
        for layer, value in self.model_dict.items():
            activate_table[layer] = np.zeros((value.shape[0], value.shape[1]))
        return activate_table

    def update_cover_dict(self):
        for key in self.temp_dict.keys():
            value = self.temp_dict[key].clone().detach().cpu().numpy()
            if len(value.shape) > 2:
                value = np.mean(
                    value, axis=tuple([i for i in range(2, len(value.shape))])
                )
            tmp_status = value > self.threshold
            # tmp_status = np.sum(tmp_status, axis=0)>0
            self.activate_table[key] = np.logical_or(
                self.activate_table[key], tmp_status
            )
        """
        for key in self.model_dict:
            temp_val = self.model_dict[key]
            temp_size = temp_val.size()
            if len(temp_size) == 4:
                temp_val = torch.flatten(temp_val, start_dim=-2, end_dim=-1)
                # scaled = scale(temp_val)
                scaled = torch.mean(temp_val, dim=2)
                scaled = scaled > self.threshold
                # scaled = torch.sum(scaled, dim=0).unsqueeze(0)
                self.coverage_table[key] = (scaled > 0)
                self.coverage_table[key] = self.coverage_table[key].cpu().detach().numpy()
            else:
                scaled = temp_val > self.threshold
                # scaled = torch.sum(scaled, dim=0).unsqueeze(0)
                self.coverage_table[key] = (scaled > 0)
                self.coverage_table[key] = self.coverage_table[key].cpu().detach().numpy()
        """

    def cal_nc(self):
        total = 0
        right = 0
        for key in self.activate_table.keys():
            neural_info = self.activate_table[key]
            sub_right_num = np.sum(neural_info, axis=-1)
            sub_total = neural_info.shape[-1]
            sub_nc = sub_right_num / neural_info.shape[-1]
            self.stat_info[key] = sub_nc
            total += sub_total
            right += sub_right_num
            self.total_info[key] = {
                "neural_info": neural_info,
                "activate_num": sub_right_num,
                "neural_num": sub_total,
                "layer_nc": sub_nc,
            }
        self.total_info["total"] = {"total_num": total, "activate_num": right}
        return right / total

    def run_once(self, data):
        if isinstance(data, torch.Tensor):
            self.model(data)
            self.activate_table = self.init_cover_dict()
            self.update_cover_dict()
            res = self.cal_nc()
            return res
        elif isinstance(data, DataLoader):
            init_flag = True
            for imgs in data:
                self.model(imgs)
                if init_flag:
                    self.activate_table = self.init_cover_dict()
                    init_flag = False
                self.update_cover_dict()
                self.c = 0
                self.temp_dict = {}
            res = self.cal_nc()
            return res


class CalNCKeras(object):
    def __init__(
        self, act_fn, model: torch.nn.Module, model_name: str, threshold: float = 0.75
    ):
        """
        calculate the neural coverage indicator for a model with one input image.
        you can add activation function name by your own
        :param model: a pytorch model
        :param threshold: threshold to justify whether a neural is activated.
        :param act_fn: which layers neurons' output you want to get.
        """
        self.model = model
        self.threshold = threshold
        self.output_nc_table = {}
        self.model_dict = {}
        self.coverage_table = {}
        self.stat_info = {}
        self.merge_flag = False
        self.model_name = model_name
        self.sub_file_lst = []
        self.check_layer_name = act_fn
        # self.check_layer_name = ['Activation', 'Conv2D', 'Dense'] # version16
        # self.check_layer_name = ['ReLU'] # version14
        self.total_info = {}

    def get_activation_layers(self, model):
        neural = set()
        for layer in model.layers:
            # if layer.__class__.__name__ == 'Activation':
            if layer.__class__.__name__ in self.check_layer_name:
                # print(layer.name, layer.__class__.__name__, layer.output_shape)
                temp_name = f"{layer.name}-{layer.__class__.__name__}"
                neural.add(temp_name)
        return neural

    def get_inter(self, model, neurals, images):
        model_dict = {}
        for item in list(neurals):
            s = item
            layer_name = s.split("-")[0]
            temp_inter = Model(
                inputs=model.input, outputs=model.get_layer(layer_name).output
            )
            temp_res = temp_inter.predict(images, verbose=0)
            if len(temp_res.shape) == 4:
                model_dict[item] = torch.Tensor(temp_res.transpose(0, 3, 1, 2))
            else:
                model_dict[item] = torch.Tensor(temp_res)
        return model_dict

    def update_coverage_point(self):
        for key in self.model_dict.keys():
            temp_val = self.model_dict[key]
            temp_val = temp_val.reshape(*temp_val.shape[:2], -1)
            # for item in temp_val:
            scaled = scale(temp_val) > self.threshold
            scaled = torch.sum(scaled, dim=0).unsqueeze(0)
            self.coverage_table[key] = scaled > 0
            self.coverage_table[key] = self.coverage_table[key].cpu().detach().numpy()
            # self.coverage_table[key] = (scaled > self.threshold)

    def update_coverage_channel(self):
        for key in self.model_dict:
            temp_val = self.model_dict[key]
            temp_size = temp_val.size()
            if len(temp_size) == 4:
                temp_val = torch.flatten(temp_val, start_dim=-2, end_dim=-1)
                # scaled = scale(temp_val)
                scaled = torch.mean(temp_val, dim=2)
                scaled = scaled > self.threshold
                # scaled = torch.sum(scaled, dim=0).unsqueeze(0)
                self.coverage_table[key] = scaled > 0
                self.coverage_table[key] = (
                    self.coverage_table[key].cpu().detach().numpy()
                )
            else:
                scaled = temp_val > self.threshold
                # scaled = torch.sum(scaled, dim=0).unsqueeze(0)
                self.coverage_table[key] = scaled > 0
                self.coverage_table[key] = (
                    self.coverage_table[key].cpu().detach().numpy()
                )

    def cal_nc(self):
        total = 0
        right = 0
        if not self.merge_flag:
            for key in self.coverage_table.keys():
                neural_info = self.coverage_table[key]
                sub_right_num = np.sum(neural_info, axis=-1)
                sub_total = neural_info.shape[-1]
                sub_nc = sub_right_num / neural_info.shape[-1]
                self.stat_info[key] = sub_nc
                total += sub_total
                right += np.sum(neural_info, axis=1)
                self.total_info[key] = {
                    "neural_info": neural_info,
                    "activate_num": sub_right_num,
                    "neural_num": sub_total,
                    "layer_nc": sub_nc,
                }
            self.total_info["total"] = {"total_num": total, "activate_num": right}
            return right / total
        else:
            # store current coverage table and merge thenm later
            save_dict = {"coverage_table": self.coverage_table}
            temp_name = save_pickle(dict=save_dict, root_dir=self.model_name)
            self.sub_file_lst.append(temp_name)
            return None

    def cal_nc_batch(self):
        total = 0
        right = 0
        if not self.merge_flag:
            for key in self.coverage_table.keys():
                neural_info = np.expand_dims(
                    np.sum(self.coverage_table[key], axis=0) > 0, axis=0
                )
                sub_right_num = np.sum(neural_info, axis=-1)
                sub_total = neural_info.shape[-1] * neural_info.shape[-2]
                sub_nc = sub_right_num / neural_info.shape[-1]
                self.stat_info[key] = sub_nc
                total += sub_total
                right += np.sum(neural_info.flatten())
                self.total_info[key] = {
                    "neural_info": neural_info,
                    "activate_num": sub_right_num,
                    "neural_num": sub_total,
                    "layer_nc": sub_nc,
                }
            self.total_info["total"] = {"total_num": total, "activate_num": right}
            return right / total
        else:
            # store current coverage table and merge thenm later
            save_dict = {"coverage_table": self.coverage_table}
            temp_name = save_pickle(dict=save_dict, root_dir=self.model_name)
            self.sub_file_lst.append(temp_name)
            return None

    def run_once(self, data):
        neurals = self.get_activation_layers(self.model)
        if isinstance(data, np.ndarray):
            self.model_dict = self.get_inter(
                model=self.model, neurals=neurals, images=data
            )
            self.update_coverage_channel()
            nc = self.cal_nc()
            return nc
        if isinstance(data, DataLoader):
            self.merge_flag = True
            for imgs in tqdm(data):
                imgs = imgs.cpu().detach().numpy()
                imgs = imgs.transpose(0, 2, 3, 1)
                self.model_dict = self.get_inter(
                    model=self.model, neurals=neurals, images=imgs
                )
                self.update_coverage_channel()
                nc = self.cal_nc_batch()
            self.coverage_table = merge_pickle(self.model_name, self.sub_file_lst)
            self.merge_flag = False
            nc = self.cal_nc_batch()
            res = {}
            res["total_nc"] = nc
            res["layers_nc"] = self.stat_info
            res["threshold"] = self.threshold
            with open(f"{self.model_name}-{self.threshold}.pkl", "wb") as f:
                pickle.dump(self.total_info, f, pickle.HIGHEST_PROTOCOL)
                f.close()
            return res
