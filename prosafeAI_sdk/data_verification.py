# -*- coding: utf-8 -*-
# @Time    : 2023/6/16 下午2:29
# @Author  : liuliping
# @File    : data_verification.py
# @description:

from prosafeAI_sdk.utils import BasicUserAuthFunc
import requests
import os
from config import ADDRS


class DataVerification(BasicUserAuthFunc):
    def __init__(self, username, password):
        super(DataVerification, self).__init__(username, password)
        self.login_status = self.login()

    def import_file(self, file_path):
        # step1: system file
        tmp_header = self.msger.base_header

        files = [
            (
                "file",
                (
                    os.path.basename(file_path),
                    open(file_path, "rb"),
                    "application/json",
                ),
            )
        ]

        req = requests.post(url=ADDRS["system_file"], headers=tmp_header, files=files)

        response = req.json()

        if response["code"] == 2000:
            return response["data"]["url"]
        else:
            return None

    def import_metadata(self, table_id, data_path, label_file_path, version_comments="MLOps pipeline"):
        # step1: system file
        file_url = self.import_file(data_path)

        # step2: import_data
        if file_url:
            tmp_header = self.msger.base_header
            tmp_msg = {
                "table_id": table_id,
                "version_comments": version_comments,
                "url": file_url,
            }

            files = [
                (
                    "label_file",
                    (
                        os.path.basename(label_file_path),
                        open(label_file_path, "rb"),
                        "application/json",
                    ),
                )
            ]

            req = requests.post(
                url=ADDRS["import_metadata"], headers=tmp_header, data=tmp_msg, files=files
            )

            response = req.json()

            if response["code"] == 2000:
                return response["data"]["data_version"]

            else:
                return response["msg"]
        else:
            return "please upload file first!"

    def create_data_verification_task(
        self, table_id, table_version, requirement_path, task_name="MLOps pipelines"
    ):
        # step1: system file
        file_url = self.import_file(requirement_path)

        # step2: import_task : requirements=-1  default import new requirements.json
        if file_url:
            tmp_header = self.msger.base_header
            tmp_msg = {
                "table": table_id,
                "table_version": table_version,
                "requirement": -1,
                "task_name": task_name,
                "json_url": file_url,
            }

            req = requests.post(
                url=ADDRS["create_data_verification"], headers=tmp_header, data=tmp_msg
            )

            response = req.json()

            if response["code"] == 2000:
                return response["data"]["task_id"]

            else:
                return response["msg"]

        else:
            return "please upload file first!"

    def run_data_verification(
        self,
        table_id,
        table_version,
        requirement_path,
        task_name="MLOps pipelines",
        task_report=None,
    ):
        # step 1: create_task
        task_id = self.create_data_verification_task(
            table_id, table_version, requirement_path, task_name
        )

        # step 2: run_task
        if isinstance(task_id, int):
            tmp_header = self.msger.base_header
            tmp_msg = {"task_id": task_id}

            req = requests.post(
                url=ADDRS["run_data_verification"], headers=tmp_header, data=tmp_msg
            )

            response = req.json()

            # step 3 : export report
            if response["code"] == 2000:
                report_response = requests.get(
                    url=f"{ADDRS['download_data_verification_report']}?task_id={task_id}",
                    headers=tmp_header,
                )

                if report_response.status_code == 200:
                    with open(
                        f"{task_report}/dataVerification_report_{task_id}.pdf", "wb"
                    ) as fw:
                        fw.write(report_response.content)

                else:
                    return report_response["msg"]

            else:
                return response["msg"]

        else:
            return task_id


if __name__ == "__main__":
    data_verification = DataVerification(username="superadmin", password="admin123456")
    data_version = data_verification.import_metadata(
        1, "./data/format_data.json", version_comments="MLOps pipelines"
    )
    if isinstance(data_version, int):
        task_result = data_verification.run_data_verification(
            1,
            data_version,
            "./data/Data-TSRClassifier.json",
            task_name="MLOps pipelines",
            task_report="./data",
        )
