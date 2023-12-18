# -*- coding: utf-8 -*-
"""
@Time ： 5/4/2023 4:56 pm
@Auth ： Jingrui Han
@File ：basicMetrics.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""

from prosafeAI_sdk.base import BaseFunc


class BasicMetrics(BaseFunc):
    def __init__(self, task_type, alg_type, token, data_path, username, password):
        super(BasicMetrics, self).__init__(
            task_type, alg_type, token, data_path, username, password
        )

    def run(self, results_path):
        # print(self.mdata_flag, self.token_flag)
        if self.mdata_flag and self.token_flag:
            self.saveResults(results_path)
        else:
            raise UserWarning("Please check your metadata or contact your admin")


if __name__ == "__main__":
    bf = BasicMetrics(
        task_type="basic_metrics",
        alg_type="classification",
        token="af7ea4c0-d773-11ed-83f7-0242ac110002",
        data_path="/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/metadata_version1",
        username="superadmin",
        password="admin123456",
    )
    bf.run(
        "/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/info_2.txt"
    )
