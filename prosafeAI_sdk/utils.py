import copy
import os
import time
import requests
import json
from prosafeAI_sdk.config import ADDRS, SUPPORTIMAGE_FORMAT


class BasicUserAuthFunc(object):
    def __init__(self, user_name, pass_word, token=None, signature=None):
        self.user_name = user_name
        self.pass_word = pass_word
        self.token = token
        self.signature = signature
        self.msger = Message(token=self.token, signature=self.signature)

    def login(self):
        tmp_header, data = self.msger.create_login_message(
            username=self.user_name, password=self.pass_word
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

    def logout(self):
        pass


def read_txt(path):
    with open(path, "r") as f:
        res = f.readlines()
    f.close()
    return res


class Message(object):
    def __init__(self, token=None, signature=None):
        self.token = token
        self.signature = signature
        self.data = {
            "token": self.token,
            # 'signature': self.signature
        }
        self.addr = ADDRS
        self.sessionid = None
        self.csrftoken = None
        self.base_header = None
        self.run_id = None

    def init_base_header(self):
        self.base_header = {
            "X-CSRFToken": self.csrftoken,
            "Cookie": f"csrftoken={self.csrftoken}; sessionid={self.sessionid}",
        }
        # print(self.sessionid, self.csrftoken, self.base_header)

    def create_login_message(self, username, password):
        header = {"Content-Type": "application/json"}
        tmp_msg = {"username": username, "password": password}
        return header, tmp_msg

    def create_run_message(self, task_type, algorithm_type, hyps: dict):
        tmp_msg, tmp_header = copy.deepcopy(self.data), copy.deepcopy(self.base_header)
        tmp_header["Content-Type"] = "application/json"
        tmp_msg["task_type"] = task_type
        tmp_msg["algorithm_type"] = algorithm_type
        tmp_msg["hyperparameter"] = hyps
        return tmp_msg, tmp_header

    def check_metadata_message(self, file_path):
        tmp_msg, tmp_header = copy.deepcopy(self.data), copy.deepcopy(self.base_header)
        # tmp_header['Content-Type'] = 'multipart/form-data'
        # tmp_msg['file_path'] = file_path
        tmp_msg["run_id"] = str(self.run_id)
        return tmp_msg, tmp_header

    def save_phased_results_message(self, results, status):
        tmp_msg = copy.deepcopy(self.data)
        tmp_header = copy.deepcopy(self.base_header)
        tmp_msg["results"] = results
        tmp_msg["status"] = status
        tmp_msg["run_id"] = self.run_id
        tmp_header["Content-Type"] = "application/json"
        return tmp_msg, tmp_header

    def save_results(self, file_path):
        tmp_msg = copy.deepcopy(self.data)
        tmp_header = copy.deepcopy(self.base_header)
        tmp_msg["run_id"] = self.run_id
        tmp_msg["signature"] = self.signature
        tmp_msg["file_path"] = file_path
        return tmp_msg, tmp_header


def find_all_file(file_path, res):
    if os.path.isdir(file_path):
        for item in os.listdir(file_path):
            if not os.path.isdir(f"{file_path}/{item}"):
                if item.split(".")[-1].lower() not in SUPPORTIMAGE_FORMAT:
                    continue
                res.append(f"{file_path}/{item}")
            else:
                find_all_file(f"{file_path}/{item}", res)
    else:
        res.append(file_path)


def create_txt(path_lst, file_name):
    with open(f"{file_name}", "w") as f:
        for path in path_lst:
            f.write(f"{path}\n")
    f.close()
