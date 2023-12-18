# -*- coding: utf-8 -*-
"""
@Time ： 24/4/2023 5:09 pm
@Auth ： Jingrui Han
@File ：utils.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""

import yaml


def decode_yaml(yaml_path):
    with open(f"{yaml_path}", "r") as f:
        dict = yaml.safe_load(f)
    f.close()
    meta_params = dict["meta_params"]
    criteria_params = dict["criteria_params"]
    run_params = dict["running_params"]
    run_params["meta_params"] = meta_params
    run_params["criteria_params"] = criteria_params
    return meta_params, criteria_params, run_params


def decode_yaml_all(yaml_path):
    with open(f"{yaml_path}", "r") as f:
        dict = yaml.safe_load(f)
    f.close()
    return dict
