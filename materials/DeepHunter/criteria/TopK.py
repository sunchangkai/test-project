import numpy as np
import tensorflow.keras as keras
import cv2
from tensorflow.keras import Model
from criteria.utils import build_dataset
from torch.utils.data import DataLoader
from PIL import Image
from collections import defaultdict
import pickle


class topK(object):
    def __init__(self, model, model_name, k, act_fn=["flatten"]):
        self.model = model
        self.model_name = model_name
        self.k = k
        self.check_layer_name = act_fn
        # self.check_layer_name = ['Activation', 'Conv2D', 'Dense'] # version16
        # self.check_layer_name = ['ReLU'] # version14
        self.model_dict = {}
        self.stat_info = {}
        self.activate_table = {}

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
            temp_res = temp_inter.predict(images)
            if len(temp_res.shape) == 4:
                model_dict[item] = temp_res.transpose(0, 3, 1, 2)
            else:
                model_dict[item] = temp_res
        return model_dict

    def init_cover_dict(self):
        activate_table = defaultdict()
        for layer, value in self.model_dict.items():
            activate_table[layer] = np.zeros((value.shape[0], value.shape[1]), np.bool)
        return activate_table

    def init_cover_dict_batch(self):
        activate_table = defaultdict()
        for layer, value in self.model_dict.items():
            activate_table[layer] = np.zeros(value.shape[1], np.bool)
        return activate_table

    def update_cover_dict(self):
        for key in self.model_dict.keys():
            value = self.model_dict[key]
            if len(value.shape) > 2:
                value = np.mean(
                    value, axis=tuple([i for i in range(2, len(value.shape))])
                )
            top_k_value = np.sort(value)[:, -self.k].reshape(value.shape[0], 1)
            top_k_value = (value - top_k_value) > 0
            self.activate_table[key] = np.logical_or(
                self.activate_table[key], top_k_value
            )

    def update_cover_dict_batch(self):
        for key in self.model_dict.keys():
            value = self.model_dict[key]
            if len(value.shape) > 2:
                value = np.mean(
                    value, axis=tuple([i for i in range(2, len(value.shape))])
                )
            top_k_value = np.sort(value)[:, -self.k].reshape(value.shape[0], 1)
            top_k_value = (value - top_k_value) >= 0
            top_k_value = np.sum(top_k_value, axis=0) > 0
            # self.topk_cover_dict[key] = top_k_value
            self.activate_table[key] = np.logical_or(
                self.activate_table[key], top_k_value
            )

    def cal_tknc(self):
        total = 0
        right = 0
        for key in self.activate_table.keys():
            temp_val = self.activate_table[key]
            sub_right = np.sum(temp_val, axis=1)
            sub_total = temp_val.shape[-1]
            total += sub_total
            right += sub_right
            self.stat_info[key] = {"top-k": temp_val, "total_neurons": sub_total}
        res = right / total
        return res

    def cal_tknc_batch(self):
        total = 0
        right = 0
        for key in self.activate_table.keys():
            temp_val = self.activate_table[key]
            sub_right = np.sum(temp_val)
            sub_total = temp_val.shape[0]
            total += sub_total
            right += sub_right
            self.stat_info[key] = {"top-k": temp_val, "total_neurons": sub_total}
        res = right / total
        return res

    def run_once(self, data):
        neurals = self.get_activation_layers(self.model)
        if isinstance(data, np.ndarray):
            self.model_dict = self.get_inter(
                model=self.model, neurals=neurals, images=data
            )
            self.activate_table = self.init_cover_dict()
            self.update_cover_dict()
            tknc = self.cal_tknc()
            return tknc
        elif isinstance(data, DataLoader):
            init_flag = True
            for images in data:
                images = images.cpu().detach().numpy()
                images = images.transpose(0, 2, 3, 1)
                self.model_dict = self.get_inter(
                    model=self.model, neurals=neurals, images=images
                )
                if init_flag:
                    self.activate_table = self.init_cover_dict_batch()
                    init_flag = False
                self.update_cover_dict_batch()
            tknc = self.cal_tknc_batch()
            return tknc
