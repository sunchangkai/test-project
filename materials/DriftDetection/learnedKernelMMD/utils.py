import os
from PIL import Image
import numpy as np
import torch


def build_dataset(path):
    names = os.listdir(path)
    data_list = []
    for name in names:
        if name.endswith("png"):
            img_file = os.path.join(path, name)
            img = Image.open(img_file)
            if img.height != 48 or img.width != 48:
                img = img.resize((48, 48))
            data = np.array(img, dtype=np.float) / 255.0
            data = data.transpose(2, 0, 1)
            # print(data.shape)
            data_list.append(data)
    data_list = np.array(data_list)
    return torch.Tensor(data_list)
