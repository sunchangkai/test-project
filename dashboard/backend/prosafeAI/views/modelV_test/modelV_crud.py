# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 下午6:10
# @Author  : liuliping
# @File    : modelV_crud.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from application.settings import (
    TASK_TYPE,
    ALGORITHM_TYPE,
    RECHARGE_QUANTITY,
    SUPPORT_MODEL_TYPE,
    ATTACK_TYPE,
    ACTIVATION_FUNC,
    BBOX_TYPE,
)
import hashlib
import datetime
from django.db import transaction
import itertools
import zipfile
import os
import pandas as pd
import shutil
from django.http import HttpResponse
import yaml
import base64
import cv2
from . import mutation_related

# import re


class ModelVCRUDViewSet(ViewSet):
    @action(methods=["get"], detail=False)
    def modelV_task_list(self, request: Request, *args, **kwargs):
        user = request.user
        task_type = request.query_params.get("task_type")
        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        if not task_type:
            return ErrorResponse(msg="task_type is required")

        try:
            sql_helper = SQLSearch()

            if not user.is_superuser:
                usercase_ids = sql_helper.search(
                    f"SELECT usercase_id from prosafeAI_usercase_member WHERE user_id={user.id}"
                )
                usercase_ids = ",".join(
                    [str(usercase["usercase_id"]) for usercase in usercase_ids]
                )

                if usercase_ids:
                    where = f"AND usercase_id in ({usercase_ids})"

                else:
                    return SuccessResponse(data=[])

            else:
                where = ""

            str_sql = f"""SELECT a.id, a.model_path, a.data_path, a.algorithm_type, a.machine_info, a.token, a.description,
            d.table_name_mysql, a.version, a.raw_hyperparameter as init_hyperparameter, a.status, DATE_FORMAT(a.create_time,'%m/%d/%Y %H:%i:%s') as create_time,
            b.`name` as usercase_name, c.`name` as project_name from prosafeAI_modelV_task as a
            JOIN prosafeAI_usercase as b ON a.usercase_id=b.id
            JOIN prosafeAI_project as c ON b.project_id=c.id
            JOIN prosafeAI_table as d ON a.table_id=d.id
            WHERE task_type='{TASK_TYPE[task_type]}' {where}
            ORDER BY a.create_time DESC;"""

            data = sql_helper.search(str_sql)
            total = len(data)
            start = (page - 1) * limit
            data = data[start : start + limit]

            return SuccessResponse(data, limit=limit, page=page, total=total)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def generate_code(self, request: Request, *args, **kwargs):
        task_id = request.query_params.get("task_id")

        user = request.user

        if not task_id:
            return ErrorResponse(msg="task_id is required")

        try:
            sql_helper = SQLSearch()

            task_info = sql_helper.search(
                str_sql=f"select * from prosafeAI_modelV_task WHERE id='{task_id}';"
            )

            if not task_info:
                return ErrorResponse(msg="task_id is error")

            task_info = task_info[0]
            used_quantity = sql_helper.search(
                str_sql=f"SELECT count(*) as count from prosafeAI_modelV_run WHERE task_id={task_id};"
            )[0]["count"]

            total_quantity = sql_helper.search(
                str_sql=f"""SELECT total_quantity from prosafeAI_modelV_token_recharge
                            WHERE task_id={task_id} ORDER BY create_time DESC LIMIT 1;"""
            )[0]["total_quantity"]

            surplus_quantity = total_quantity - used_quantity

            json_text = {
                "001_Female_20_Afternoon_Anger_ir_00054.png": [
                    {
                        "bbox": [
                            433.6870085964,
                            171.5398192259,
                            495.5488704582,
                            263.4317111178,
                        ],
                        "class": "0",
                        "confidence": 0.91,
                    },
                    {
                        "bbox": [
                            423.6870085964,
                            161.5398192259,
                            485.5488704582,
                            273.4317111178,
                        ],
                        "class": "0",
                        "confidence": 0.8,
                    },
                    {
                        "bbox": [
                            225.6870085964,
                            80.5398192259,
                            307.5488704582,
                            376.4317111178,
                        ],
                        "class": "1",
                        "confidence": 0.9,
                    },
                ]
            }

            sample_code = {
                "basic_metrics_classification": f"""# step2: import package and run task.
from prosafeAI_sdk.basicMetrics import BasicMetrics
basic_metrics_task = BasicMetrics(task_type={task_info['task_type']}, alg_type={task_info['algorithm_type']},
                  token={task_info['token']},
                  data_path={task_info['data_path']},
                  username={user}, password='please input your password')
# your_prediction_result.txt is the result file of model inference, including absolute path of the image and prediction， separated by commas.
# eg:
# /img/img_train_0.png,0
# /img/img_train_1.png,0
# ...  
basic_metrics_task.run('your_prediction_result.txt')""",
                "basic_metrics_object_detection": f"""# step2: import package and run task.
from prosafeAI_sdk.basicMetrics import BasicMetrics
basic_metrics_task = BasicMetrics(task_type={task_info['task_type']}, alg_type={task_info['algorithm_type']},
                  token={task_info['token']},
                  data_path={task_info['data_path']},
                  username={user}, password='please input your password')
# your_prediction_result.json is the result file of model inference, including image name and prediction.
# eg:
{json_text}

basic_metrics_task.run('your_prediction_result.json)""",
                "robustness_classification": f"""# step3: import package and run task.
from prosafeAI_sdk.robustnessTest import RobustnessTest
robustness_test_task = RobustnessTest(task_type={task_info['task_type']}, alg_type={task_info['algorithm_type']},
                  token={task_info['token']},
                  data_path={task_info['data_path']},
                  username={user}, password='please input your password')

# hyps_all.yaml was downloaded from the previous step. 
robustness_test_task.run('/hyps/hyps_all.yaml')
""",
                "robustness_object_detection": f"""# step3: import package and run task.
# hyps_all.yaml was downloaded from the previous step. 
from prosafeAI_sdk.robustnessTest import RobustnessTest
robustness_test_task = RobustnessTest(task_type={task_info['task_type']}, alg_type={task_info['algorithm_type']},
                  token={task_info['token']},
                  data_path={task_info['data_path']},
                  username={user}, password='please input your password',
                  hyp_path=/hyps/hyps_all.yaml)

robustness_test_task.run()
""",
            }

            return DetailResponse(
                data={
                    "token": task_info["token"],
                    "code": sample_code[
                        f'{task_info["task_type"]}_{task_info["algorithm_type"]}'
                    ],
                    "remaining_times": surplus_quantity,
                    "hyperparameter": task_info["init_hyperparameter"],
                }
            )

        except Exception as e:
            return ErrorResponse(e.__str__())

    @action(methods=["get"], detail=False)
    def modelV_run_list(self, request: Request, *args, **kwargs):
        task_id = request.query_params.get("task_id")
        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        if not task_id:
            return ErrorResponse(msg="task_id is required")

        try:
            sql_helper = SQLSearch()

            task_info = sql_helper.search(
                str_sql=f"select * from prosafeAI_modelV_task WHERE id='{task_id}';"
            )

            if not task_info:
                return ErrorResponse(msg="task_id is error")

            task_type = task_info[0]["task_type"]

            data = sql_helper.search(
                str_sql=f"""SELECT a.id, a.task_id, a.hyperparameter, b.model_path, b.data_path, b.algorithm_type,
                            b.machine_info, b.token, b.description, b.table_id, b.version,
                            DATE_FORMAT(a.start_time,'%m/%d/%Y %H:%i:%s') as start_time
                            from prosafeAI_modelV_run as a
                            JOIN prosafeAI_modelV_task as b ON a.task_id=b.id
                            WHERE a.task_id='{task_id}'
                            ORDER BY a.start_time DESC;"""
            )

            if task_type == TASK_TYPE["0"]:  # if robustness,  add process_rate
                # process_rate, status

                for sub in data:
                    step_info = sql_helper.search(
                        str_sql=f"SELECT * from prosafeAI_modelV_step WHERE run_id={sub['id']} ORDER BY process_rate DESC;"
                    )
                    now = datetime.datetime.now()

                    check_info = sql_helper.search(
                        str_sql=f"SELECT * from prosafeAI_modelV_check_report WHERE run_id={sub['id']};"
                    )

                    start_time = check_info[0]["create_time"]

                    if step_info:  # running
                        first_item_time = step_info[-1]["create_time"]
                        last_item_time = step_info[0]["create_time"]
                        process_rate = (
                            step_info[0]["process_rate"]
                            if step_info[0]["process_rate"]
                            else 0
                        )

                        if process_rate < 0.99:
                            if now.timestamp() - last_item_time.timestamp() > 10 * (
                                first_item_time.timestamp() - start_time.timestamp()
                            ):
                                sub["status"] = 0

                            else:
                                sub["status"] = 1

                            sub["process_rate"] = process_rate

                        else:
                            sub["process_rate"] = 1
                            sub["status"] = 2

                    else:  # pending
                        if (
                            now.timestamp() - start_time.timestamp() > 2000 * 60 * 60
                        ):  # > 2h
                            sub["status"] = 0

                        else:
                            sub["status"] = 1

                        sub["process_rate"] = 0

            total = len(data)
            start = (page - 1) * limit
            data = data[start : start + limit]

            return SuccessResponse(data, limit=limit, page=page, total=total)

        except Exception as e:
            return ErrorResponse(e.__str__())

    @action(methods=["get"], detail=False)
    def quick_modelV_run(self, request: Request, *args, **kwargs):
        task_type = request.query_params.get("task_type")
        limit = int(request.query_params.get("limit", 3))
        page = int(request.query_params.get("page", 1))

        if not task_type:
            return ErrorResponse(msg="task_type is required")

        try:
            sql_helper = SQLSearch()
            data = sql_helper.search(
                str_sql=f"""SELECT a.id, a.task_id, a.hyperparameter, b.model_path, b.data_path, b.algorithm_type,
                            b.machine_info, b.token, b.description, b.table_id, b.version,
                            DATE_FORMAT(a.start_time,'%m/%d/%Y %H:%i:%s') as start_time
                            from prosafeAI_modelV_run as a
                            JOIN prosafeAI_modelV_task as b ON a.task_id=b.id
                            WHERE a.task_type='{TASK_TYPE[task_type]}'
                            ORDER BY a.start_time DESC
                            limit 3;"""
            )

            return SuccessResponse(data, limit=limit, page=page, total=len(data))

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["post"], detail=False)
    @transaction.atomic  #
    def create_task(self, request: Request, *args, **kwargs):
        table_id = request.data.get("table")
        table_version = request.data.get("table_version")
        task_type = request.data.get("task_type")
        model_path = request.data.get("model_path")
        data_path = request.data.get("data_path")
        raw_hyperparameter = request.data.get("init_hyperparameter", {})
        alg_type = request.data.get("algorithm_type")
        machine_info = request.data.get("machine_info")
        description = request.data.get("description")

        if not (
            table_id
            and table_version
            and task_type
            and model_path
            and data_path
            and alg_type
            and description
        ):
            return ErrorResponse(
                msg="table/table_version/task_type/model_path/data_path/alg_type/description is required"
            )

        if task_type == "1" and not machine_info:
            return ErrorResponse(msg="machine_info is required")

        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            token = hashlib.md5(now.encode("utf-8")).hexdigest()

            sql_helper = SQLSearch()

            usercase_id = sql_helper.search(
                str_sql=f"SELECT usercase_id from prosafeAI_table WHERE id={table_id};"
            )[0]["usercase_id"]

            raw_hyperparameter = eval(str(raw_hyperparameter))

            if task_type == "0":  # robustness  generate hyperparameter
                # model_framework = requset.data.get('model_framework')
                # dataset_format = requset.data.get('dataset_format')

                # if not (model_framework and dataset_format and not domain):
                #     return ErrorResponse(msg='model_framework/dataset_format/domain is required')

                hyperparameter = {
                    "running_param": {
                        "img_dir": data_path,
                        "model_path": model_path,
                        # "dataset_format": raw_hyperparameter['dataset_format'],
                        "dl_frame": raw_hyperparameter["model_framework"],
                        # "task_type": TASK_TYPE[task_type],
                    }
                }

                if raw_hyperparameter["model_type"] == "white box":
                    hyperparameter["criteria"] = [
                        raw_hyperparameter["mutation_guidance"]
                    ]
                    hyperparameter["project"] = (
                        f"{os.path.basename(model_path)}-r{str(raw_hyperparameter['r'])}-ktime{str(raw_hyperparameter['k_time'])}-maxitem{str(raw_hyperparameter['max_iter'])}-alpha{str(raw_hyperparameter['alpha'])}-beta{str(raw_hyperparameter['beta'])}-{datetime.datetime.now().timestamp()}",
                    )

                label_map = sql_helper.search(
                    str_sql=f"SELECT label_map from prosafeAI_version  WHERE table_id={table_id} and version={table_version};"
                )

                if label_map[0]["label_map"]:
                    class_num = len(eval(label_map[0]["label_map"]))

                for key, value in raw_hyperparameter.items():
                    if key == "mutation_guidance":
                        # activation_function map

                        for sub_key, sub_val in raw_hyperparameter[
                            "mutation_params"
                        ].items():
                            if sub_key == "act_fn":
                                format_act_func = []
                                for act_fn in sub_val:
                                    format_act_func.append(
                                        ACTIVATION_FUNC[
                                            raw_hyperparameter["model_framework"]
                                        ].get(act_fn)
                                    )

                                hyperparameter.setdefault(
                                    "criteria_params", {}
                                ).setdefault(value, {}).setdefault(
                                    sub_key, format_act_func
                                )

                            else:
                                hyperparameter.setdefault(
                                    "criteria_params", {}
                                ).setdefault(value, {}).setdefault(sub_key, sub_val)

                        hyperparameter["criteria_params"][value].setdefault(
                            "model_name", os.path.basename(model_path)
                        )

                    elif key in {
                        "mutation_params",
                        "domain",
                        "model_framework",
                        "model_type",
                        "bbox_type",
                        "scale",
                    }:
                        continue

                    elif "level" in key or "corruption" in key:
                        for sub_data in value:
                            parameter = {}

                            if sub_data["method"] == "vertical_flip":
                                parameter = {"a": [0, 5], "dtype": "int"}

                            elif sub_data["method"] in {"mirror", "poisson_noise"}:
                                parameter = {"b": [0, 5], "dtype": "int"}

                            else:
                                for param in sub_data["parameters"]:
                                    value = (
                                        [eval(sub) for sub in param["value"].split(",")]
                                        if "," in param["value"]
                                        else eval(param["value"])
                                    )

                                    parameter.setdefault(param["name"], value)
                                    parameter.setdefault("dtype", param["dtype"])

                                if sub_data["method"] in {"IFGSM", "FGSM"}:
                                    parameter["class_num"] = class_num

                            hyperparameter.setdefault("meta_params", {}).setdefault(
                                sub_data["method"], parameter
                            )

                    else:
                        hyperparameter.setdefault("running_param", {}).setdefault(
                            key, value
                        )

            else:  # basic_metrics
                if alg_type == "1":
                    hyperparameter = {
                        "scale": raw_hyperparameter["scale"],
                        "bbox_type": BBOX_TYPE.get(
                            raw_hyperparameter["bbox_type"], "XYWH"
                        ),
                    }
                else:
                    raw_hyperparameter = hyperparameter = ""

            task_id = sql_helper.insert(
                str_sql=f"""INSERT INTO prosafeAI_modelV_task (table_id, version, task_type, model_path, data_path, 
                raw_hyperparameter, init_hyperparameter, algorithm_type, machine_info, description, usercase_id, 
                create_time, token, status) VALUES 
                ('{table_id}', '{table_version}', '{TASK_TYPE[task_type]}', '{model_path}', '{data_path}', 
                "{str(raw_hyperparameter)}",  "{str(hyperparameter)}", '{ALGORITHM_TYPE[alg_type]}', '{machine_info}', 
                '{description}', '{usercase_id}', '{now}', '{token}', '0');"""
            )

            # recharge token, default=20

            sql_helper.insert(
                str_sql=f"""INSERT INTO prosafeAI_modelV_token_recharge (recharge_quantity, create_time, total_quantity, task_id) 
                VALUES ('{RECHARGE_QUANTITY}', '{now}', '{RECHARGE_QUANTITY}', '{task_id}');"""
            )

            return DetailResponse(msg="success", data={"task_id": task_id})

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def download_report(self, request: Request, *args, **kwargs):
        from django.utils.encoding import escape_uri_path
        from prosafeAI.views.modelV_test.modelV_report import (
            basic_metrics_report,
            robustness_report,
        )

        run_id = request.query_params.get("run_id")

        if not run_id:
            return ErrorResponse(msg="run_id is required")

        try:
            sql_helper = SQLSearch()
            str_sql = f"""
                SELECT a.`id` as run_id, a.`task_type`, c.`model_path`, c.`data_path`, c.`machine_info`, c.`create_time`, 
                c.`id` as task_id, c.raw_hyperparameter, a.status, a.result_path, a.`celery_result` as result FROM prosafeAI_modelV_run a
                JOIN prosafeAI_modelV_task c on a.`task_id`=c.`id`  
                WHERE a.`id`={run_id}
            """
            data = sql_helper.search(str_sql)

            # filename = ""

            if data[0]["status"] == "FAILURE":
                return ErrorResponse(msg=f"run task failed! {data[0]['traceback']}")

            if not data[0]["result"]:
                return ErrorResponse(msg="please run the task or wait for completion")

            # if data:
            #     if data[0]['status'] == 'SUCCESS':
            if data[0]["task_type"] == "basic_metrics":
                filename = f"""basic_metrics_report_{run_id}.pdf"""
                basic_metrics_report(filename, data)
                path = os.path.join(os.getcwd(), filename)
            elif data[0]["task_type"] == "robustness":
                filename = f"""robustness_report_{run_id}.pdf"""
                robustness_report(filename, data)
                path = os.path.join(os.getcwd(), filename)
            else:
                return ErrorResponse(
                    msg="The task_type should be basic metrics or robustness."
                )

            #     else:
            #         return ErrorResponse(msg='This run is failed. Please re-run the task')
            # else:
            #     return ErrorResponse(msg='Please run the task or wait for results')

            with open(path, "rb") as f:
                response = HttpResponse(content_type="application/pdf;charset=utf-8")
                response["Access-Control-Expose-Headers"] = "Content-Disposition"
                response[
                    "Content-Disposition"
                ] = "attachment;filename*=UTF-8''{}".format(escape_uri_path(filename))
                response.write(f.read())
                return response

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def review_code(self, request: Request, *args, **kwargs):
        run_id = request.query_params.get("run_id")
        user = request.user

        if not run_id:
            return ErrorResponse(msg="run_id is required")

        try:
            sql_helper = SQLSearch()

            run_info = sql_helper.search(
                str_sql=f"""SELECT a.task_type, a.hyperparameter, b.algorithm_type, token, data_path from prosafeAI_modelV_run as a 
                    JOIN prosafeAI_modelV_task as b 
                    ON a.task_id=b.id
                    WHERE a.id={run_id};"""
            )[0]

            json_text = {
                "001_Female_20_Afternoon_Anger_ir_00054.png": [
                    {
                        "bbox": [
                            433.6870085964,
                            171.5398192259,
                            495.5488704582,
                            263.4317111178,
                        ],
                        "class": "0",
                        "confidence": 0.91,
                    },
                    {
                        "bbox": [
                            423.6870085964,
                            161.5398192259,
                            485.5488704582,
                            273.4317111178,
                        ],
                        "class": "0",
                        "confidence": 0.8,
                    },
                    {
                        "bbox": [
                            225.6870085964,
                            80.5398192259,
                            307.5488704582,
                            376.4317111178,
                        ],
                        "class": "1",
                        "confidence": 0.9,
                    },
                ]
            }

            sample_code = {
                "basic_metrics_classification": f"""# step2: import package and run task.
from prosafeAI_sdk.basicMetrics import BasicMetrics
basic_metrics_task = BasicMetrics(task_type={run_info['task_type']}, alg_type={run_info['algorithm_type']},
                  token={run_info['token']},
                  data_path={run_info['data_path']},
                  username={user}, password='please input your password')
# your_prediction_result.txt is the result file of model inference, including absolute path of the image and prediction， separated by commas.
# eg:
# /img/img_train_0.png,0
# /img/img_train_1.png,0
# ...  
basic_metrics_task.run('your_prediction_result.txt')""",
                "basic_metrics_object_detection": f"""# step2: import package and run task.
from prosafeAI_sdk.basicMetrics import BasicMetrics
basic_metrics_task = BasicMetrics(task_type={run_info['task_type']}, alg_type={run_info['algorithm_type']},
                  token={run_info['token']},
                  data_path={run_info['data_path']},
                  username={user}, password='please input your password')
# your_prediction_result.json is the result file of model inference, including image name and prediction.
# eg:
{json_text}

basic_metrics_task.run('your_prediction_result.json)""",
                "robustness_classification": f"""# step3: import package and run task.
from prosafeAI_sdk.robustnessTest import RobustnessTest
robustness_test_task = RobustnessTest(task_type={run_info['task_type']}, alg_type={run_info['algorithm_type']},
                  token={run_info['token']},
                  data_path={run_info['data_path']},
                  username={user}, password='please input your password')

# hyps_all.yaml was downloaded from the previous step. 
robustness_test_task.run('/hyps/hyps_all.yaml')
""",
                "robustness_object_detection": f"""# step3: import package and run task.
# hyps_all.yaml was downloaded from the previous step. 
from prosafeAI_sdk.robustnessTest import RobustnessTest
robustness_test_task = RobustnessTest(task_type={run_info['task_type']}, alg_type={run_info['algorithm_type']},
                  token={run_info['token']},
                  data_path={run_info['data_path']},
                  username={user}, password='please input your password',
                  hyp_path=/hyps/hyps_all.yaml)

robustness_test_task.run()
""",
            }

            return DetailResponse(
                data={
                    "code": sample_code[
                        f'{run_info["task_type"]}_{run_info["algorithm_type"]}'
                    ],
                    # "hyperparameter": hyperparameter[f'{run_info["task_type"]}_{run_info["algorithm_type"]}'],
                    "hyperparameter": run_info["hyperparameter"],
                }
            )

        except Exception as e:
            return ErrorResponse(e.__str__())

    @action(methods=["post"], detail=False)
    def view_basic_metrics(self, request: Request, *args, **kwargs):
        run_id = request.data.get("run_id")
        detail = request.data.get("detail")

        if not (run_id and detail):
            return ErrorResponse(msg="run_id/detail is required")

        try:
            sql_helper = SQLSearch()

            celery_result = sql_helper.search(
                str_sql=f"""SELECT b.algorithm_type, a.status, a.traceback, a.celery_result from 
                            prosafeAI_modelV_run a JOIN prosafeAI_modelV_task b on a.task_id=b.id
                            WHERE a.id={run_id}"""
            )

            if celery_result[0]["status"] == "FAILURE":
                return ErrorResponse(
                    msg=f"run task failed! {celery_result[0]['traceback']}"
                )

            if not celery_result[0]["celery_result"]:
                return ErrorResponse(msg="please run the task or wait for completion")

            algorithm_type = celery_result[0]["algorithm_type"]

            celery_result = eval(celery_result[0]["celery_result"])

            labels = celery_result["labels"]
            labels = self.replace_label(run_id, labels)

            basic_metrics = celery_result["basic_metrics"]

            result = []

            if algorithm_type == "classification":
                for sub in detail:
                    sub["average"] = (
                        sub.get("average", "weighted")
                        if sub["metrics"] != "accuracy"
                        else sub.get("average", "balance")
                    )

                    sub["value"] = basic_metrics[f'{sub["average"]}*{sub["metrics"]}']
                    result.append(sub)

                result.append(
                    {
                        "metrics": "matrix",
                        "detail": self.format_matrix(
                            basic_metrics["matrix"], length=len(labels)
                        ),
                        "labels": labels,
                    }
                )

            elif algorithm_type == "object_detection":
                iou = request.data.get("iou", 0.5)

                for sub in detail:
                    if sub["metrics"] != "mAP":
                        sub["average"] = sub.get("average", "weighted")

                        sub["value"] = basic_metrics[iou][
                            f'{sub["average"]}*{sub["metrics"]}'
                        ]
                    else:
                        sub["value"] = basic_metrics[iou]["mAP"]

                    result.append(sub)

            return DetailResponse(data=result)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["post"], detail=False)
    def view_slices_basic_metrics(self, request: Request, *args, **kwargs):
        run_id = request.data.get("run_id")
        detail = request.data.get("detail")
        fields = request.data.get("fields")

        if not (run_id and detail and fields):
            return ErrorResponse(msg="run_id/detail/fields is required")

        try:
            sql_helper = SQLSearch()

            celery_result = sql_helper.search(
                str_sql=f"""SELECT b.algorithm_type, a.status, a.traceback, a.celery_result from 
                            prosafeAI_modelV_run a JOIN prosafeAI_modelV_task b on a.task_id=b.id
                            WHERE a.id={run_id}"""
            )

            if celery_result[0]["status"] == "FAILURE":
                return ErrorResponse(
                    msg=f"run task failed! {celery_result[0]['traceback']}"
                )

            if not celery_result[0]["celery_result"]:
                return ErrorResponse(msg="please run the task or wait for completion")

            algorithm_type = celery_result[0]["algorithm_type"]

            celery_result = eval(celery_result[0]["celery_result"])

            labels = celery_result["labels"]
            labels = self.replace_label(run_id, labels)
            final_result = []

            if algorithm_type == "classification":
                exchange = False

                field_length = len(fields)

                if field_length == 1:
                    slices_basic_metrics = celery_result["slices_basic_metrics"][
                        "one_odd"
                    ][fields[0]]
                elif field_length == 2:
                    slices_basic_metrics = celery_result["slices_basic_metrics"][
                        "two_odd"
                    ].get(f"{fields[0]}*{fields[1]}", {})

                    if not slices_basic_metrics:
                        slices_basic_metrics = celery_result["slices_basic_metrics"][
                            "two_odd"
                        ].get(f"{fields[1]}*{fields[0]}", {})

                        exchange = True

                else:
                    return ErrorResponse(msg="odd number < 3")

                matrix = []
                for idx, sub in enumerate(detail):
                    average = (
                        sub.get("average", "weighted")
                        if sub["metrics"] != "accuracy"
                        else sub.get("average", "balance")
                    )

                    result = {"average": average, "metrics": sub["metrics"]}

                    for key, slice_detail in slices_basic_metrics.items():
                        if key == "values":
                            result["values"] = slice_detail
                            continue

                        if field_length == 1:
                            result.setdefault("detail", []).append(
                                {
                                    "odd1": key,
                                    "value": slice_detail[
                                        f'{average}*{sub["metrics"]}'
                                    ],
                                }
                            )
                            if idx == 0:
                                matrix.append(
                                    {
                                        "odd1": key,
                                        "detail": self.format_matrix(
                                            slice_detail["matrix"], length=len(labels)
                                        ),
                                    }
                                )
                        else:  # two odd
                            odds = (
                                key.split("*")
                                if not exchange
                                else list(reversed(key.split("*")))
                            )
                            result.setdefault("detail", []).append(
                                {
                                    "odd1": odds[0],
                                    "odd2": odds[1],
                                    "value": slice_detail[
                                        f'{average}*{sub["metrics"]}'
                                    ],
                                }
                            )
                            if idx == 0:
                                matrix.append(
                                    {
                                        "odd1": odds[0],
                                        "odd2": odds[1],
                                        "detail": self.format_matrix(
                                            slice_detail["matrix"], length=len(labels)
                                        ),
                                    }
                                )

                    final_result.append(result)

                final_result.append(
                    {"metrics": "matrix", "labels": labels, "detail": matrix}
                )

            elif algorithm_type == "object_detection":
                iou = request.data.get("iou", 0.5)
                field_type = request.data.get("field_type")

                if not field_type:
                    return ErrorResponse(msg="field_type is required")

                if field_type == "0":  # class切片
                    slices_basic_metrics = celery_result["basic_metrics"][iou]["detail"]

                    slice_data = [
                        slice
                        for slice in slices_basic_metrics
                        if slice["class"] == fields[0]
                    ][0]

                    for sub in detail:
                        sub["average"] = (
                            sub.get("average", "weighted")
                            if sub["metrics"] != "AP"
                            else ""
                        )

                        sub["value"] = slice_data[sub["metrics"]]

                        final_result.append(sub)

                    final_result.append(
                        {
                            "metrics": "PR-curve",
                            "detail": {
                                "x": slice_data["interpolated recall"],
                                "y": slice_data["interpolated precision"],
                            },
                        }
                    )

                elif field_type == "1":  # odd slice
                    slices_basic_metrics = celery_result["slices_basic_metrics"][
                        fields[0]
                    ]

                    for sub in detail:
                        average = (
                            sub.get("average", "weighted")
                            if sub["metrics"] != "mAP"
                            else ""
                        )

                        result = {"average": average, "metrics": sub["metrics"]}

                        for key, slice_detail in slices_basic_metrics.items():
                            if key == "values":
                                result["values"] = slice_detail
                                continue

                            result.setdefault("detail", []).append(
                                {
                                    "odd1": key,
                                    "value": slice_detail[iou][
                                        f'{average}*{sub["metrics"]}'
                                    ]
                                    if average
                                    else slice_detail[iou]["mAP"],
                                }
                            )

                        final_result.append(result)

            return DetailResponse(data=final_result)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def attack_method_info(self, request: Request, *args, **kwargs):
        model_type = request.query_params.get("model_type", 0)
        attack_type = request.query_params.get("attack_type")

        if not (model_type and attack_type):
            return ErrorResponse(msg="model_type/attack_type is required")

        if model_type not in SUPPORT_MODEL_TYPE:
            return ErrorResponse(msg="Unsupported model_type")

        if attack_type not in ATTACK_TYPE:
            return ErrorResponse(msg="Unsupported attack_type")

        try:
            sql_helper = SQLSearch()

            attack_methods = sql_helper.search(
                str_sql=f"""SELECT `method`, `parameter`, `description` FROM prosafeAI_modelV_attack_method WHERE attack_type='{ATTACK_TYPE[attack_type]}' 
                            AND support_model LIKE '%{SUPPORT_MODEL_TYPE[model_type]}%';"""
            )

            attack_methods = [
                {
                    "method": method["method"],
                    "parameter": eval(method["parameter"]),
                    "description": method["description"],
                }
                for method in attack_methods
            ]

            return DetailResponse(data=attack_methods)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["post"], detail=False)
    def view_robustness_metrics(self, request: Request, *args, **kwargs):
        run_id = request.data.get("run_id")
        detail = request.data.get("detail")

        if not (run_id and detail):
            return ErrorResponse(msg="run_id/detail is required")

        try:
            sql_helper = SQLSearch()

            celery_result = sql_helper.search(
                str_sql=f"""SELECT status, traceback, celery_result from prosafeAI_modelV_run
                                           WHERE id={run_id}"""
            )

            if celery_result[0]["status"] == "FAILURE":
                return ErrorResponse(
                    msg=f"run task failed! {celery_result[0]['traceback']}"
                )

            if not celery_result[0]["celery_result"]:
                return ErrorResponse(msg="please run the task or wait for completion")

            celery_result = eval(celery_result[0]["celery_result"])

            result = []

            if len(detail) == 1:
                aspect = detail[0].get("aspect")

                if aspect == "0":  # category
                    data = celery_result["label_slices"]

                elif aspect == "1":
                    data = celery_result["method_slices"]

                else:
                    return ErrorResponse(
                        msg="Please choose another aspect to analysis together"
                    )

                data = sorted(data.items(), key=lambda x: x[1]["ASR"], reverse=True)

                other_attack = 0
                other_success = 0

                for idx, (key, val) in enumerate(data):
                    del val["distance_detail"]
                    del val["attack_failed"]

                    if idx >= 5:
                        other_attack += val["attack_samples"]
                        other_success += val["attack_success"]

                    else:
                        result.append({"slice": key, "detail": val})

                if other_success:
                    result.append(
                        {
                            "slice": "other",
                            "detail": {
                                "attack_samples": other_attack,
                                "attack_success": other_success,
                            },
                        }
                    )

                return DetailResponse(data=result)

            elif len(detail) == 2:
                if (
                    detail[0]["aspect"] != "2" and detail[1]["aspect"] != "2"
                ):  # category method
                    for key1, key2 in itertools.product(
                        detail[0]["choose"], detail[1]["choose"]
                    ):
                        if detail[0]["aspect"] == "0":
                            key = f"{key1}*{key2}"
                        else:
                            key = f"{key2}*{key1}"

                        data = celery_result["label_method_slices"][key]

                        del data["distance_detail"]
                        del data["ASR"]
                        del data["attack_samples"]

                        result.append({"slice": key, "detail": data})

                    return DetailResponse(data=result)

                elif detail[0]["aspect"] in {"0", "2"} and detail[1]["aspect"] in {
                    "0",
                    "2",
                }:  # category distance
                    if detail[0]["aspect"] == "0":
                        choose = detail[0].get("choose")
                        distance = detail[1]["choose"]
                    else:
                        choose = detail[1].get("choose")
                        distance = detail[0]["choose"]

                    xiax = list(
                        celery_result["total_distance"]["distance_detail"][
                            distance
                        ].keys()
                    )

                    if not choose:
                        data = celery_result["total_distance"]["distance_detail"][
                            distance
                        ]

                        result.append({"slice": "total", "y": list(data.values())})

                    else:
                        for label in choose:
                            data = celery_result["label_slices"][label][
                                "distance_detail"
                            ][distance]

                            result.append({"slice": label, "y": list(data.values())})

                    return DetailResponse(data={"x": xiax, "detail": result})

                elif detail[0]["aspect"] in {"1", "2"} and detail[1]["aspect"] in {
                    "1",
                    "2",
                }:  # method distance
                    if detail[0]["aspect"] == "1":
                        choose = detail[0]["choose"]
                        distance = detail[1]["choose"]
                    else:
                        choose = detail[1]["choose"]
                        distance = detail[0]["choose"]

                    xiax = list(
                        celery_result["total_distance"]["distance_detail"][
                            distance
                        ].keys()
                    )

                    for method in choose:
                        data = celery_result["method_slices"][method][
                            "distance_detail"
                        ][distance]

                        result.append({"slice": method, "detail": list(data.values())})

                    return DetailResponse(data={"x": xiax, "detail": result})

                else:
                    return ErrorResponse(msg="aspect is unsupported")

            else:
                return ErrorResponse(msg="choose error")

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def get_run_labels(self, request: Request, *args, **kwargs):
        run_id = request.query_params.get("run_id")

        if not run_id:
            return ErrorResponse(msg="run_id is required")

        try:
            labels = self.replace_label(run_id)

            return DetailResponse(data=labels)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def get_run_attack_methods(self, request: Request, *args, **kwargs):
        run_id = request.query_params.get("run_id")

        if not run_id:
            return ErrorResponse(msg="run_id is required")

        try:
            sql_helper = SQLSearch()

            run_result = sql_helper.search(
                str_sql=f"SELECT hyperparameter, result_path from prosafeAI_modelV_run WHERE id={run_id}"
            )

            if not run_result[0]["hyperparameter"]:
                return ErrorResponse(msg="no hyperparameter")

            if not run_result[0]["result_path"]:
                return ErrorResponse(msg="please run the task or wait for completion")

            hyperparameter = eval(run_result[0]["hyperparameter"])
            result_path = run_result[0]["result_path"]

            attack_methods = list(hyperparameter["meta_params"].keys())

            unzip_path = result_path.replace(".zip", "")

            with zipfile.ZipFile(result_path) as file:
                file.extractall(unzip_path)

            for root_path, dir, files in os.walk(unzip_path):
                if dir:
                    with open(
                        os.path.join(root_path, dir[0], "all_records.txt"),
                        "r",
                        encoding="utf-8",
                    ) as f:
                        all_records = f.readlines()

            data = pd.DataFrame(
                [
                    {
                        sub.split(":")[0]: sub.split(":")[1]
                        for sub in line.strip().split(",")
                    }
                    for line in all_records
                ]
            )

            used_methods = data["mutated_method"].drop_duplicates().tolist()

            result_method = []

            for method in attack_methods:
                if method in used_methods:  #
                    result_method.append({"name": method, "disable": 0})

                else:
                    result_method.append({"name": method, "disable": 1})

            return DetailResponse(data=result_method)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def view_attack_sample_info(self, request: Request, *args, **kwargs):
        run_id = request.query_params.get("run_id")
        method = request.query_params.get("method")
        label = request.query_params.get("label")
        pred_label = request.query_params.get("pred_label")
        attack_status = request.query_params.get("attack_status")
        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        if not run_id:
            return ErrorResponse(msg="run_id is required")

        sql_helper = SQLSearch()

        result_path = sql_helper.search(
            str_sql=f"SELECT result_path from prosafeAI_modelV_run WHERE id={run_id}"
        )

        if not result_path[0]["result_path"]:
            return ErrorResponse(msg="please run the task or wait for completion")

        result_path = result_path[0]["result_path"]

        unzip_path = result_path.replace(".zip", "")

        with zipfile.ZipFile(result_path) as file:
            file.extractall(unzip_path)

        for root_path, dir, files in os.walk(unzip_path):
            if dir:
                with open(
                    os.path.join(root_path, dir[0], "all_records.txt"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    all_records = f.readlines()

        data = pd.DataFrame(
            [
                {
                    sub.split(":")[0]: sub.split(":")[1]
                    for sub in line.strip().split(",")
                }
                for line in all_records
            ]
        )

        shutil.rmtree(unzip_path)

        if method:
            data = data[data["mutated_method"] == method]

        if label:
            data = data[data["label"] == label]

        if pred_label:
            data = data[data["pred_label"] == pred_label]

        if attack_status:
            data = data[data["attack_status"] == attack_status]

        data = data.to_dict("records")

        total = len(data)

        start = (page - 1) * limit

        data = data[start : start + limit]

        return SuccessResponse(data=data, page=page, limit=limit, total=total)

    @action(methods=["get"], detail=False)
    def download_hyperparameter(self, request: Request, *args, **kwargs):
        task_id = request.query_params.get("task_id")

        if not task_id:
            return ErrorResponse(msg="task_id is required")

        try:
            sql_helper = SQLSearch()

            init_hyperparameter = sql_helper.search(
                str_sql=f"SELECT init_hyperparameter from prosafeAI_modelV_task WHERE id={task_id}"
            )

            if not init_hyperparameter[0]["init_hyperparameter"]:
                return ErrorResponse(
                    msg="The task is not rubostness. Please recreate the task"
                )

            hyperparameter = eval(init_hyperparameter[0]["init_hyperparameter"])

            response = HttpResponse(content_type="application/yaml;charset=utf-8")
            response["Access-Control-Expose-Headers"] = "Content-Disposition"
            response["Content-Disposition"] = "attachment;filename=hyperparameter.yaml"
            response.write(yaml.dump(hyperparameter))

            return response

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def download_attack_sample(self, request: Request, *args, **kwargs):
        run_id = request.query_params.get("run_id")

        if not run_id:
            return ErrorResponse(msg="run_id is required")

        try:
            sql_helper = SQLSearch()

            result_path = sql_helper.search(
                str_sql=f"SELECT result_path from prosafeAI_modelV_run WHERE id={run_id}"
            )

            if not result_path[0]["result_path"]:
                return ErrorResponse(msg="please run the task or wait for completion")

            result_path = result_path[0]["result_path"]

            unzip_path = result_path.replace(".zip", "")

            with zipfile.ZipFile(result_path) as file:
                file.extractall(unzip_path)

            response = HttpResponse(content_type="application/text;charset=utf-8")
            response["Access-Control-Expose-Headers"] = "Content-Disposition"
            response["Content-Disposition"] = "attachment;filename=all_records.txt"

            for root_path, dir, files in os.walk(unzip_path):
                if dir:
                    # with open(os.path.join(root_path, dir[0], 'all_records.txt'), 'r', encoding='utf-8') as f:
                    #     all_records = f.readlines()

                    with open(
                        os.path.join(root_path, dir[0], "all_records.txt"), "r"
                    ) as f:
                        response.write(f.read())

                    break

            return response

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["post"], detail=False)
    def mutation_image(self, request: Request, *args, **kwargs):
        method = request.data.get("method", "")
        params = request.data.get("params", {})

        try:
            # IMG_FOLDER_PATH = "static/rest_framework/img"
            img = cv2.imread("static/rest_framework/img/test_image.jpg")

            if method:  # mutation image
                img = mutation_related.__dict__[method](img=img, params=params)

            retval, img_buffer = cv2.imencode(".png", img)

            image_base = base64.b64encode(img_buffer)
            data = {
                "image": "data:image/png;base64," + image_base.decode("utf-8"),
            }

            return DetailResponse(data=data)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["post"], detail=False)
    @transaction.atomic
    def save_hyperparamter_template(self, request: Request, *args, **kwargs):
        user = request.user
        hyperparameter = request.data.get("init_hyperparameter")
        name = request.data.get("template_name")
        description = request.data.get("template_description")

        if not (hyperparameter or name or description):
            return ErrorResponse(
                msg="init_hyperparameter/template_name/template_description is required"
            )

        try:
            sql_helper = SQLSearch()

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            template_id = sql_helper.insert(
                str_sql=f"""INSERT INTO prosafeAI_modelV_hyperparamter_template (`name`, content, description, create_time,
                user_id)
                    VALUES ('{name}', '{hyperparameter}', '{description}', '{now}', '{user.id}');"""
            )

            return DetailResponse(msg="success", data={"id": template_id})

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    def hyperparamter_template_list(self, request: Request, *args, **kwargs):
        user = request.user
        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        try:
            sql_helper = SQLSearch()

            str_sql = f"""SELECT * from prosafeAI_modelV_hyperparamter_template WHERE user_id={user.id}
            ORDER BY create_time DESC;"""

            data = sql_helper.search(str_sql)
            total = len(data)
            start = (page - 1) * limit
            data = data[start : start + limit]

            return SuccessResponse(data, limit=limit, page=page, total=total)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["get"], detail=False)
    @transaction.atomic
    def delete_hyperparamter_template(self, request: Request, *args, **kwargs):
        id = int(request.query_params.get("id"))

        if not id:
            return ErrorResponse("id is required")

        try:
            sql_helper = SQLSearch()

            str_sql = f"""delete from prosafeAI_modelV_hyperparamter_template WHERE id={id};"""

            data = sql_helper.delete(str_sql)

            return (
                DetailResponse(msg="success") if data else DetailResponse(msg="failed")
            )

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @staticmethod
    def replace_label(run_id, labels=None):
        if labels is None:
            labels = []

        sql_helper = SQLSearch()
        label_map = sql_helper.search(
            str_sql=f"""SELECT c.label_map from prosafeAI_modelV_run as a
                                JOIN prosafeAI_modelV_task as b ON a.task_id=b.id
                                JOIN prosafeAI_version as c ON b.table_id=c.table_id
                                WHERE a.id={run_id} and c.version=b.version;"""
        )[0]

        label_map = eval(label_map["label_map"])

        if labels:
            for idx, label in enumerate(labels):
                if label in label_map.keys():
                    labels[idx] = label_map[label]
        else:
            labels = [{"idx": key, "category": val} for key, val in label_map.items()]

        return labels

    @staticmethod
    def format_matrix(matrix, length):
        if matrix[0]:
            format_matrix = []
            for i in range(length):
                for j in range(length):
                    format_matrix.append([i, j, int(matrix[i][j])])

            return format_matrix

        else:
            return matrix
