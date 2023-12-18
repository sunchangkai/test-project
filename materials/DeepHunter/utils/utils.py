import numpy
import os
import yaml
import numpy as np
import json


def decode_res(res):
    temp_res = np.argmax(res, axis=1)
    return temp_res


def create_folder(project):
    os.makedirs(project)
    print(f"{project} has been created!")
    os.makedirs(f"{project}/saved")
    print(f"saved folder has been created")
    os.makedirs(f"{project}/fail_test")
    print(f"fail_set folder has been created")


def decode_yaml(yaml_path):
    with open(f"{yaml_path}", "r") as f:
        dict = yaml.safe_load(f)
    f.close()
    meta_params = dict["meta_params"]
    criteria_params = dict["criteria_params"]
    return meta_params, criteria_params


def store_label_json(dict: dict, path: str):
    j_data = json.dumps(dict, indent=2)
    with open(path, "w") as f:
        f.write(j_data)
    f.close()
