import cv2
from criteria.criterial_strategy import CriteriaStrategy
import tensorflow.keras as keras
import numpy as np
import os

criteria_params = {
    "TopK": {"k": 5, "act_fn": ["ReLU"]},
    "KMNC": {
        "k_section": 1000,
        "train_data_path": "../data/test_1/0",
        "act_fn": ["ReLU"],
    },
    "NC": {"threshold": 0.75, "act_fn": ["ReLU"]},
}
model_path = "../models/v14/tsr_classifier_model.h5"
model = keras.models.load_model(model_path)
calculator = CriteriaStrategy(
    criteria=["TopK", "NC"], model=model, params=criteria_params
)
for item in os.listdir("../data/test_1/4"):
    if not item.endswith("png"):
        continue
    t_img = cv2.imread(f"../data/test_1/4/{item}")
    t_img = np.expand_dims(t_img, axis=0)
    res = calculator.calculate(img=t_img, model_name="ttttt")
    print(res)
