import os
import numpy as np
import cv2
from alibi_detect.cd import MMDDrift
from alibi_detect.utils.pytorch import GaussianRBF
from time import time
from PIL import Image


def load_dataset(path):
    names = os.listdir(path)
    data_list = []
    for name in names:
        if name.endswith("png"):
            img_file = os.path.join(path, name)
            img = Image.open(img_file)
            if img.height != 48 or img.width != 48:
                img = img.resize((48, 48))
            data = np.array(img, dtype=np.float) / 255.0
            # data = data.transpose(2, 0, 1)
            # print(data.shape)
            data_list.append(data)
    data_list = np.array(data_list)
    # return torch.Tensor(data_list)
    return data_list


def MMD_drift_detection(ref_path, test_path, model_name):
    # build dataset: numpy to tensor
    # send features of ref and test to MMDDrift
    # get result
    # build dataset: numpy to tensor

    load_s_time = time()
    ref_dataset = load_dataset(path=ref_path)
    test_dataset = load_dataset(path=test_path)
    load_time = time() - load_s_time

    # extract features
    ext_s_time = time()
    ref_features = ref_dataset
    test_features = test_dataset
    ext_time = time() - ext_s_time

    # send features of ref and test to MMDDrift
    det_s_time = time()
    cd = MMDDrift(ref_features, backend="pytorch", p_val=0.05, kernel=GaussianRBF)
    preds = cd.predict(test_features, return_p_val=True, return_distance=True)
    det_time = time() - det_s_time
    preds["performance"] = {
        "loading_time": load_time,
        "ext_feature_time": ext_time,
        "det_time": det_time,
        "model_name": model_name,
    }
    return preds


if __name__ == "__main__":
    res = MMD_drift_detection(
        ref_path="../test/china_negative/china_negative_100_0_sample1",
        test_path="../test/china_negative/china_negative_100_0_sample1",
        model_name="no",
    )
    print(res)
