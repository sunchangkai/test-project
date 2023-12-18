from .utils import build_dataset
from alibi_detect.cd import MMDDrift
from alibi_detect.utils.pytorch import GaussianRBF
from time import time


def MMD_drift_detection(ref_path, test_path, feature_extractor, model_name):
    # build dataset: numpy to tensor
    # send features of ref and test to MMDDrift
    # get result
    # build dataset: numpy to tensor

    load_s_time = time()
    ref_dataset = build_dataset(path=ref_path)
    test_dataset = build_dataset(path=test_path)
    load_time = time() - load_s_time

    # extract features
    ext_s_time = time()
    ref_features = feature_extractor(ref_dataset).detach().numpy()
    test_features = feature_extractor(test_dataset).detach().numpy()
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
