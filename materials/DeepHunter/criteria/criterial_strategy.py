import numpy as np

from criteria.KMNC import cal_kmnc
from criteria.TopK import topK
from criteria.neuron_coverage import cal_nc
from criteria.neuron_sensitivity import NeuronSensitivity
from criteria.utils import build_dataset


class CriteriaStrategy(object):
    def __init__(self, criteria: list, model, params):
        self.criteria = criteria
        if not self.criteria:
            self.criteria = ["TopK"]
        print(f"{self.criteria} would be calculated!")
        self.model = model
        self.params = params

    def calculate(self, img, model_name):
        res = {}
        if "TopK" in self.criteria:
            k = self.params["TopK"]["k"]
            topk_act_fn = self.params["TopK"]["act_fn"]
            topk_calculator = topK(
                model=self.model, model_name=model_name, k=k, act_fn=topk_act_fn
            )
            topk_val = topk_calculator.run_once(data=img[0])
            res["TopK"] = topk_val

        if "KMNC" in self.criteria:
            k_section = self.params["KMNC"]["k_section"]
            train_data_path = self.params["KMNC"]["train_data_path"]
            kmnc_act_fn = self.params["KMNC"]["act_fn"]
            kmnc_res = []
            kmnc_calculator = cal_kmnc(
                k_section=k_section,
                model_name=model_name,
                model=self.model,
                train_dataset=build_dataset(dir_path=train_data_path),
                act_fn=kmnc_act_fn,
            )
            for image in img[0]:
                image = np.expand_dims(image, axis=0)
                kmnc_val = kmnc_calculator.run_once(test_dataset=image)
                kmnc_res.append(kmnc_val)
            res["KMNC"] = kmnc_res

        if "NC" in self.criteria:
            threshold = self.params["NC"]["threshold"]
            nc_act_fn = self.params["NC"]["act_fn"]
            nc_calculator = cal_nc(
                model=self.model,
                model_name=model_name,
                threshold=threshold,
                act_fn=nc_act_fn,
            )
            nc_val = nc_calculator.run_once(data=img[0])
            res["NC"] = nc_val

        if "NeuronSensitivity" in self.criteria:
            threshold = self.params["NeuronSensitivity"]["threshold"]
            act_fn = self.params["NeuronSensitivity"]["act_fn"]
            ns_calculator = NeuronSensitivity(
                model=self.model,
                model_name=model_name,
                threshold=threshold,
                act_fn=act_fn,
            )
            ns_val = ns_calculator.run_once(o_data=img[0], m_data=img[1])
            res["NeuronSensitivity"] = ns_val
        return res
