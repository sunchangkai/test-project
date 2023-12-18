# -*- coding: utf-8 -*-
"""
@Time ： 5/4/2023 3:42 pm
@Auth ： Jingrui Han
@File ：base.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""
# import copy
import os
import time
from utils import Message, create_txt, find_all_file, read_txt
import requests
from config import ADDRS  # , SUPPORTIMAGE_FORMAT
import json


class BaseFunc(object):
    def __init__(
        self, task_type, alg_type, token, data_path, username, password, signature=None
    ):
        self.task_type_dict = {"robustness": "0", "basic_metrics": "1"}
        self.flag_dict = {"failed": False, "success": True}
        self.token = token
        self.task_type = task_type
        self.alg_type = alg_type
        self.data_path = data_path
        self.msger = Message(token=self.token)
        self.username = username
        self.password = password
        self.login_flag = self.login()
        self.token_flag = self.create_run()
        self.mdata_flag = self.checkMetaData()
        # self.token_flag = 1
        # self.mdata_flag = 1

    def login(self):
        tmp_header, data = self.msger.create_login_message(
            username=self.username, password=self.password
        )
        data = json.dumps(data)
        req = requests.Session()
        req.post(url=ADDRS["login"], headers=tmp_header, data=data)
        tmp_cookie = req.cookies.get_dict()
        try:
            self.msger.csrftoken = tmp_cookie["csrftoken"]
            self.msger.sessionid = tmp_cookie["sessionid"]
            self.msger.init_base_header()
            print("Login Success")
            return True
        except Exception:
            raise Exception("Login failed")

    def create_run(self):
        data, header = self.msger.create_run_message(
            task_type=self.task_type_dict[self.task_type],
            algorithm_type=self.alg_type,
            hyps={11: 11},
        )
        req = requests.post(
            url=f"{ADDRS['create_run']}", headers=header, data=json.dumps(data)
        )
        # req = requests.request(method='POST', url=ADDRS['create_run'], headers=header, data=json.dumps(data))
        # print('create_run', req.json())
        try:
            self.msger.run_id = int(req.json().get("data")["run_id"])
            # print('run_id', self.msger.run_id)
            print(f"Create running record success! Your Run ID is {self.msger.run_id}")
            return True
        except Exception:
            print(f"Create running record failed! The progress would be terminated")
            return False
        # return req.json().get('msg')

    def checkMetaData(self):
        # find all data
        print(f"Start searching valid files under {self.data_path}")
        all_files = []
        find_all_file(file_path=self.data_path, res=all_files)
        print(f"{len(all_files)} files has been found!")
        # generate data to txt
        self.metadata_file_name = f"{self.msger.token}-{time.time()}.txt"
        create_txt(path_lst=all_files, file_name=self.metadata_file_name)
        # files = [
        #     ('file', (self.data_path, open(self.data_path, 'rb'), 'text/plain'))
        # ]
        files = [
            (
                "file",
                (
                    self.metadata_file_name,
                    open(self.metadata_file_name, "rb"),
                    "text/plain",
                ),
            )
        ]
        data, header = self.msger.check_metadata_message(self.data_path)
        # req = requests.request(method='POST', url=ADDRS['check_metadata'], headers=header, data=data, files=files)
        req = requests.post(
            url=ADDRS["check_metadata"], data=data, headers=header, files=files
        )
        tmp_flag = self.flag_dict[req.json().get("msg")]
        if tmp_flag:
            print(f"Catch the valid metadata set!")
        else:
            print(
                f"Cannot find correct metadata set, please check your dataset or create the new metadata!"
            )
        return self.flag_dict[req.json().get("msg")]

    def postPhaseResults(self, results):
        # only available for robustness
        status = 0
        tmp_msg, header = self.msger.save_phased_results_message(
            results=results, status=status
        )
        if self.task_type == "robustness":
            req = requests.post(
                url=ADDRS["save_phased_results"],
                headers=header,
                data=json.dumps(tmp_msg),
            )
            print(req.json())
            return req.json().get("msg")
        else:
            raise NotImplementedError(f"Currently not support ---<{self.task_type}>")

    def saveResults(self, result_path):
        self.result_path = result_path
        tmp_msg, tmp_header = self.msger.save_results(file_path=result_path)
        if self.task_type == "robustness":
            os.system(f"zip {result_path}/results.zip -r {result_path}")
            req = requests.post(
                url=f"{ADDRS['save_results']}",
                data=self.msger.save_results(result_path),
                files={"file": open(f"{result_path}/result.zip", "rb")},
            )
            return req.json().get("msg")

        elif self.task_type == "basic_metrics":
            # ========================================
            self.check_result_valid()
            # ========================================
            files = {"file": open(result_path, "rb")}
            req = requests.post(
                url=f"{ADDRS['save_results']}",
                data=tmp_msg,
                headers=tmp_header,
                files=files,
            )
            print("Save results", req.json().get("msg"))
            return req.json().get("msg")

        else:
            raise NotImplementedError(f"Currently not support ---<{self.task_type}>")

    def check_result_valid(self):
        # check the validation of result
        m_ll = read_txt(path=self.metadata_file_name)
        r_ll = read_txt(path=self.result_path)
        m_names = []
        r_names = []
        r_labels = []
        # check length
        if len(m_ll) != len(r_ll):
            raise Exception(f"The length of dataset cannot match the results!")
        else:
            for i in range(len(m_ll)):
                m_names.append(m_ll[i].split()[0].split("/")[-1].strip("\n"))
                r_names.append(r_ll[i].split()[0].split("/")[-1].strip("\n"))
                r_labels.append(r_ll[i].split()[-1].strip("\n"))
            # check the corresponding relation between metadata and results
            if set(m_names) != set(r_names):
                raise Exception(f"Your dataset cannot match your results!")
            try:
                list(map(int, r_labels))
            except Exception:
                raise ValueError(f"Invalid results exist on you results!")


if __name__ == "__main__":
    bf = BaseFunc(
        task_type="basic_metrics",
        alg_type="classification",
        token="af7ea4c0-d773-11ed-83f7-0242ac110002",
        data_path="/Users/jingruihan/Desktop/prosafeAI/MIK/val_script/baidu_val",
        username="superadmin",
        password="admin123456",
    )
    # bf.login()
    # bf.create_run()
    # bf.checkMetaData()
    # bf.postPhaseResults(results={"criteria": "test", "iteration": "20", "fail_test_num": "10", "total_mutator": "30", "ASR": "0.9"})
    bf.saveResults(result_path="info.txt")
    # res = []
    # file_path = '/Users/jingruihan/Desktop/prosafeAI/MIK/val_script/baidu_val'
    # find_all_file(file_path, res)
    # for item in res:
    #     print(item)
