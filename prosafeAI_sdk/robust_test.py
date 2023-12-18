# -*- coding: utf-8 -*-
"""
@Time ： 5/4/2023 4:55 pm
@Auth ： Jingrui Han
@File ：robustnessTest.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""
import time
from prosafeAI_sdk.base import BaseFunc
from prosafeAI_sdk.robustness_test.main import TestingFramework
from prosafeAI_sdk.__utils import decode_yaml


class RobustnessTest(BaseFunc):
    def __init__(
        self, task_type, alg_type, token, data_path, username, password, hyp_path
    ):
        self.hyps_path = hyp_path
        super().__init__(task_type, alg_type, token, data_path, username, password)
        # self.token = token
        # self.task_type = task_type
        # self.alg_type = alg_type
        # self.msger = Message(token=self.token)
        # self.data_path = data_path

        # check token
        # self.token_flag = self.create_run()
        # self.token_flag = 1
        # check metadata
        # self.mdata_flag = self.checkMetaData(data_path)
        # self.mdata_flag = 1

    def run(self):
        # all_params = decode_yaml(self.hyps_path)
        if self.token_flag and self.mdata_flag:
            # self.result_dir = 'metadata_version1'
            # for tmp_res in [{"criteria": "test", "iteration": "20", "fail_test_num": "10", "total_mutator": "30", "ASR": "0.9"} for i in range(10)]:
            #     self.postPhaseResults(tmp_res)
            # todo: run test
            _, __, running_params = decode_yaml(self.hyps_path)
            # self.result_dir = running_params['project']
            self.func = TestingFramework(**running_params)
            for res in self.func.run():
                rr = res
                try:
                    self.postPhaseResults(rr)
                except Exception:
                    continue
            # self.func = ddp().run()
            # for res in self.func:
            #     self.postPhaseResults(res)
            # while 1:
            #     print(self.func.__next__())
            self.saveResults(result_path=self.func.project)


class ddp(object):
    def __init__(self):
        self.iter = 10
        self.tmp_res = {
            "criteria": "test",
            "iteration": "20",
            "fail_test_num": "10",
            "total_mutator": "30",
            "ASR": "0.9",
        }

    def run(self):
        for i in range(self.iter):
            time.sleep(3)
            yield self.tmp_res


if __name__ == "__main__":
    rr = RobustnessTest(
        task_type="robustness",
        alg_type="classification",
        # token='123456',
        token="83ccf36ed786c48a2804ed15199eb021",
        # data_path='/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/metadata_version1',
        data_path="/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/data/train_self_newer",
        username="superadmin",
        password="admin123456",
        hyp_path="/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/hyps/hyps_all.yaml",
    )
    rr.run()
