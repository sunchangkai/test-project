import torch
import numpy as np
from criteria.utils import build_dataset, save_pickle, merge_pickle, scale
from torch.utils.data import DataLoader
from tqdm import tqdm
from tensorflow.keras import Model
import tensorflow.keras as keras
import pickle
import cv2


class cal_nc(object):
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
