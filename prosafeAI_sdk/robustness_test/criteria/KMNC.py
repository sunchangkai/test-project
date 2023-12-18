# -*- coding: utf-8 -*-
"""
@Time ： 20/2/2023 1:47 pm
@Auth ： Jingrui Han
@File ：KMNC.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""
import copy

import torch
from keras import Model
import numpy as np
from prosafeAI_sdk.robustness_test.utils.others import build_dataset
import cv2
from torch.utils.data import DataLoader
from PIL import Image
from tqdm import tqdm
import os
from collections import defaultdict
import pickle


class CalKMNCTorch(object):
    def __init__(self, k_section, model_name, model, train_data_path, act_fn):
        self.interval = defaultdict()
        self.model = model
        self.model_name = model_name
        self.k = k_section
        self.train_dataset = build_dataset(train_data_path)
        self.train_model_dict = {}
        self.act_fn = act_fn
        self.temp_model_dict = self.get_model_dict(self.model)
        # self.check_layer_name = ['Activation', 'Conv2D', 'Dense'] # version16
        # self.check_layer_name = ['ReLU'] # version 14
        self.upper_bounds, self.lower_bounds = self.get_boundary()
        # output_intern({'upper': self.upper_bounds, 'lower': self.lower_bounds}, f"boundary-{model_name}")
        for keys in self.upper_bounds.keys():
            self.interval[keys] = (
                self.upper_bounds[keys] - self.lower_bounds[keys]
            ) / self.k
        # output_intern({'interval': self.interval}, f"interval-{model_name}")
        self.test_model_dict = {}
        self.activation_table = self.init_activation_table()

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
                    self.temp_dict[temp_name] = output.clone().detach().cpu().numpy()
                else:
                    self.temp_dict[name] = output.clone().detach().cpu().numpy()
                    self.c = 1

            return hook

        for name, layer in model.named_modules():
            if name in neurons:
                # print(name)
                layer.register_forward_hook(set_table(name))
        return self.temp_dict

    def get_boundary(self):
        # global temp_model_dict
        lower_bounds = {}
        upper_bounds = {}
        for imgs in self.train_dataset:
            # imgs = imgs.cpu().detach().numpy()
            self.model(imgs)
            # temp_model_dict = self.get_model_dict(self.model)
            for layer, value in self.temp_model_dict.items():
                # value = value.cpu().detach().numpy()
                value = np.mean(
                    value, axis=tuple([i for i in range(2, len(value.shape))])
                )
                min_value = np.min(value, axis=0)
                max_value = np.max(value, axis=0)
                if layer in lower_bounds:
                    max_flag = upper_bounds[layer] > max_value
                    min_flag = lower_bounds[layer] < min_value
                    upper_bounds[layer] = upper_bounds[layer] * max_flag + max_value * (
                        1 - max_flag
                    )
                    lower_bounds[layer] = lower_bounds[layer] * min_flag + min_value * (
                        1 - min_flag
                    )
                else:
                    upper_bounds[layer] = max_value
                    lower_bounds[layer] = min_value
        self.train_model_dict = copy.deepcopy(self.temp_model_dict)
        return upper_bounds, lower_bounds

    def init_activation_table(self):
        """Initial the activate table."""
        activate_section_table = defaultdict()
        for layer, value in self.train_model_dict.items():
            activate_section_table[layer] = np.zeros((value.shape[1], self.k), np.bool)
        return activate_section_table

    def update_cover_dict(self):
        for key in self.test_model_dict:
            temp_val = self.test_model_dict[key]
            temp_val = np.mean(
                temp_val, axis=tuple([i for i in range(2, len(temp_val.shape))])
            )
            hits = np.floor(
                (temp_val - self.lower_bounds[key]) / self.interval[key]
            ).astype(int)
            hits = np.transpose(hits, [1, 0])
            for n in range(len(hits)):
                for sec in hits[n]:
                    if sec >= self.k or sec < 0:
                        continue
                    self.activation_table[key][n][sec] = True
        with open(f"{self.model_name}-{self.k}-act_table.pkl", "wb") as f:
            pickle.dump(self.activation_table, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    def cal_kmnc(self):
        total_neurons = 0
        activated_neurons = 0
        for _, value in self.activation_table.items():
            sub_right = np.sum(value)
            activated_neurons += sub_right
            total_neurons += len(value)
        activate_rate = activated_neurons / total_neurons
        return activate_rate / self.k

    def run_once(self, data):
        if isinstance(data, torch.Tensor):
            self.model(data)
            self.activate_table = self.init_activation_table()
            self.update_cover_dict()
            res = self.cal_kmnc()
            return res
        elif isinstance(data, DataLoader):
            init_flag = True
            for imgs in data:
                self.model(imgs)
                if init_flag:
                    self.activate_table = self.init_activation_table()
                    init_flag = False
                self.update_cover_dict()
                self.c = 0
                self.temp_dict = {}
            res = self.cal_kmnc()
            return res


class CalKMNCKeras(object):
    def __init__(self, k_section, model_name, model, train_data_path, act_fn):
        self.interval = defaultdict()
        self.model = model
        self.model_name = model_name
        self.k = k_section
        self.train_dataset = build_dataset(train_data_path)
        self.train_model_dict = {}
        self.check_layer_name = act_fn
        # self.check_layer_name = ['Activation', 'Conv2D', 'Dense'] # version16
        # self.check_layer_name = ['ReLU'] # version 14
        self.upper_bounds, self.lower_bounds = self.get_boundary()
        # output_intern({'upper': self.upper_bounds, 'lower': self.lower_bounds}, f"boundary-{model_name}")
        for keys in self.upper_bounds.keys():
            self.interval[keys] = (
                self.upper_bounds[keys] - self.lower_bounds[keys]
            ) / self.k
        # output_intern({'interval': self.interval}, f"interval-{model_name}")
        self.test_model_dict = {}
        self.activation_table = self.init_activation_table()

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
                model_dict[item] = temp_res.transpose(0, 3, 1, 2)
            else:
                model_dict[item] = temp_res
        return model_dict

    def init_activation_table(self):
        """Initial the activate table."""
        activate_section_table = defaultdict()
        for layer, value in self.train_model_dict.items():
            activate_section_table[layer] = np.zeros((value.shape[1], self.k), np.bool)
        return activate_section_table

    def get_boundary(self):
        lower_bounds = {}
        upper_bounds = {}
        for imgs in self.train_dataset:
            imgs = imgs.cpu().detach().numpy()
            imgs = imgs.transpose(0, 2, 3, 1)
            neurons = self.get_activation_layers(self.model)
            temp_model_dict = self.get_inter(self.model, neurons, imgs)
            for layer, value in temp_model_dict.items():
                value = np.mean(
                    value, axis=tuple([i for i in range(2, len(value.shape))])
                )
                min_value = np.min(value, axis=0)
                max_value = np.max(value, axis=0)
                if layer in lower_bounds:
                    max_flag = upper_bounds[layer] > max_value
                    min_flag = lower_bounds[layer] < min_value
                    upper_bounds[layer] = upper_bounds[layer] * max_flag + max_value * (
                        1 - max_flag
                    )
                    lower_bounds[layer] = lower_bounds[layer] * min_flag + min_value * (
                        1 - min_flag
                    )
                else:
                    upper_bounds[layer] = max_value
                    lower_bounds[layer] = min_value
        self.train_model_dict = temp_model_dict
        return upper_bounds, lower_bounds

    def update_cover_dict(self):
        for key in self.test_model_dict:
            temp_val = self.test_model_dict[key]
            temp_val = np.mean(
                temp_val, axis=tuple([i for i in range(2, len(temp_val.shape))])
            )
            hits = np.floor(
                (temp_val - self.lower_bounds[key]) / self.interval[key]
            ).astype(int)
            hits = np.transpose(hits, [1, 0])
            for n in range(len(hits)):
                for sec in hits[n]:
                    if sec >= self.k or sec < 0:
                        continue
                    self.activation_table[key][n][sec] = True
        with open(f"{self.model_name}-{self.k}-act_table.pkl", "wb") as f:
            pickle.dump(self.activation_table, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    def cal_kmnc(self):
        total_neurons = 0
        activated_neurons = 0
        for _, value in self.activation_table.items():
            sub_right = np.sum(value)
            activated_neurons += sub_right
            total_neurons += len(value)
        activate_rate = activated_neurons / total_neurons
        return activate_rate / self.k

    def run_once(self, test_dataset):
        neurons = self.get_activation_layers(self.model)
        if isinstance(test_dataset, np.ndarray):
            self.test_model_dict = self.get_inter(self.model, neurons, test_dataset)
            self.update_cover_dict()
            # output_intern({'activation': self.activation_table}, f"activation-{self.model_name}")
            kmnc = self.cal_kmnc()
            return kmnc
        elif isinstance(test_dataset, DataLoader):
            for imgs in test_dataset:
                imgs = imgs.cpu().detach().numpy()
                imgs = imgs.transpose(0, 2, 3, 1)
                self.test_model_dict = self.get_inter(self.model, neurons, imgs)
                self.update_cover_dict()
            # output_intern({'activation': self.activation_table}, f"activation-{self.model_name}")
            kmnc = self.cal_kmnc()
            return kmnc