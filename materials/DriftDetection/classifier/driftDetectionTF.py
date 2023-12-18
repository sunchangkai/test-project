import os
import time
import numpy as np
import torch
from PIL import Image
import tensorflow as tf
from alibi_detect.cd import ClassifierDrift
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Input


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
            data_list.append(data)

    return np.array(data_list)


def init_classifier_graph():
    model = tf.keras.Sequential(
        [
            Input(shape=(48, 48, 3)),
            Conv2D(8, 4, strides=2, padding="same", activation=tf.nn.relu),
            Conv2D(16, 4, strides=2, padding="same", activation=tf.nn.relu),
            Conv2D(32, 4, strides=2, padding="same", activation=tf.nn.relu),
            Flatten(),
            Dense(2, activation="softmax"),
        ]
    )

    return model


# def init_classifier_graph():
#     model = torch.nn.Sequential(
#         torch.nn.Conv2d(in_channels=3, out_channels=8, stride=2, kernel_size=(4,4)),
#         torch.nn.ReLU(),
#         torch.nn.Conv2d(in_channels=8, out_channels=16, stride=2, kernel_size=(4, 4)),
#         torch.nn.ReLU(),
#         torch.nn.Conv2d(in_channels=16, out_channels=32, stride=2, kernel_size=(4, 4)),
#         torch.nn.ReLU(),
#         torch.nn.Flatten(),
#         torch.nn.Linear(in_features=512, out_features=2)
#     )
#     return model


def drift_detect_with_classifier(ref_path, test_path):
    l_start = time.time()
    ref_set = build_dataset(ref_path)
    test_set = build_dataset(test_path)
    # image_num = ref_set.shape[0]
    load_time = time.time() - l_start

    model_graph = init_classifier_graph()
    i_start_time = time.time()
    cd = ClassifierDrift(
        ref_set, model_graph, p_val=0.05, train_size=0.5, epochs=10, verbose=True
    )
    preds = cd.predict(test_set)
    infer_time = time.time() - i_start_time

    preds["performance"] = {
        "loading_time": load_time,
        "ext_feature_time": 0,
        "det_time": infer_time,
        "model_name": "self_trained",
    }
    return preds
