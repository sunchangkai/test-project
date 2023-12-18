# -*- coding: utf-8 -*-
"""
@Time ： 20/2/2023 2:43 pm
@Auth ： Jingrui Han
@File ：NS.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""
import copy

import numpy as np
import keras
import cv2
from keras import Model
from torch.utils.data import DataLoader
from PIL import Image
from collections import defaultdict
import torch


class CalNSKeras(object):
    def __init__(self, model, model_name, threshold=0.5, act_fn=["flatten"], e=None):
        self.model = model
        self.model_name = model_name
        self.threshold = threshold
        self.check_layer_name = act_fn

        self.o_model_dict = {}
        self.m_model_dict = {}
        self.stat_info = {}
        self.activate_table = {}

    def normalize(self, x):
        # utility function to normalize a tensor by its L2 norm
        return np.sqrt(np.mean(np.square(x), axis=(1, 2, 3))) + 1e-5

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

    def init_cover_dict(self):
        activate_table = defaultdict()
        for layer, value in self.o_model_dict.items():
            # activate_table[layer] = np.zeros(value.shape[1], np.bool)
            activate_table[layer] = np.zeros((value.shape[0], value.shape[1]), np.bool)
        return activate_table

    def update_cover_dict(self):
        for key in self.o_model_dict:
            o_output = self.o_model_dict[key]
            m_output = self.m_model_dict[key]
            if len(o_output.shape) > 2 and len(m_output.shape) > 2:
                o_output = np.mean(
                    o_output, axis=tuple([i for i in range(2, len(o_output.shape))])
                )
                m_output = np.mean(
                    m_output, axis=tuple([i for i in range(2, len(m_output.shape))])
                )
            # diff = o_output-m_output
            l2_norm = np.expand_dims(self.normalize(self.diff), axis=1)
            ns = (o_output - m_output) / l2_norm
            temp_act_table = ns > self.threshold
            self.activate_table[key] = np.logical_or(
                self.activate_table[key], temp_act_table
            )
        pass

    def cal_ns(self):
        total = 0
        right = 0
        for key in self.activate_table:
            temp_val = self.activate_table[key]
            sub_right = np.sum(temp_val, axis=1)
            right += sub_right
            sub_total = temp_val.shape[1]
            total += sub_total
        res = right / total
        return res

    def run_once(self, o_data, m_data):
        neurals = self.get_activation_layers(self.model)
        if isinstance(o_data, np.ndarray) and isinstance(m_data, np.ndarray):
            self.diff = o_data - m_data
            self.o_model_dict = self.get_inter(
                self.model, neurals=neurals, images=o_data
            )
            self.m_model_dict = self.get_inter(
                self.model, neurals=neurals, images=m_data
            )
            self.activate_table = self.init_cover_dict()
            self.update_cover_dict()
            res = self.cal_ns()
            return res


class CalNSTorch(object):
    def __init__(self, model, model_name, threshold, act_fn=["flatten"], e=None):
        self.model = model
        self.model_name = model_name
        self.threshold = threshold
        self.act_fn = act_fn
        self.model_dict = self.get_model_dict(self.model)
        self.o_model_dict = {}
        self.m_model_dict = {}
        self.stat_info = {}
        self.activate_table = {}

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

    def init_cover_dict(self):
        activate_table = defaultdict()
        for layer, value in self.model_dict.items():
            activate_table[layer] = np.zeros((value.shape[0], value.shape[1]), np.bool)
        return activate_table

    def normalize(self, x):
        # utility function to normalize a tensor by its L2 norm
        return np.sqrt(np.mean(np.square(x), axis=(1, 2, 3))) + 1e-5

    def update_cover_dict(self):
        for key in self.o_model_dict:
            o_output = self.o_model_dict[key]
            m_output = self.m_model_dict[key]
            if len(o_output.shape) > 2 and len(m_output.shape) > 2:
                o_output = np.mean(
                    o_output, axis=tuple([i for i in range(2, len(o_output.shape))])
                )
                m_output = np.mean(
                    m_output, axis=tuple([i for i in range(2, len(m_output.shape))])
                )
            l2_norm = np.expand_dims(self.normalize(self.diff), axis=1)
            ns = (m_output - o_output) / l2_norm
            temp_act_table = ns > self.threshold
            self.activate_table[key] = np.logical_or(
                self.activate_table[key], temp_act_table
            )
        pass

    def cal_ns(self):
        total = 0
        right = 0
        for key in self.activate_table:
            temp_val = self.activate_table[key]
            sub_right = np.sum(temp_val, axis=-1)
            right += sub_right
            sub_total = temp_val.shape[1]
            total += sub_total
        res = right / total
        return res

    def run_once(self, o_data, m_data):
        if isinstance(o_data, torch.Tensor) and isinstance(m_data, torch.Tensor):
            self.diff = (o_data - m_data).clone().detach().cpu().numpy()
            self.model(o_data)
            self.o_model_dict = copy.deepcopy(self.temp_dict)
            self.temp_dict = {}
            self.model(m_data)
            self.m_model_dict = copy.deepcopy(self.temp_dict)
            self.activate_table = self.init_cover_dict()
            self.update_cover_dict()
            res = self.cal_ns()
            return res
