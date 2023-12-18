# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 下午5:52
# @Author  : liuliping
# @File    : modelV_sdk_view.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
import datetime
from django.db import transaction
import os
from application.settings import TASK_TYPE, BBOX_TYPE
from prosafeAI import tasks


class ModelVSDKViewSet(ViewSet):
    @action(methods=["post"], detail=False)
    @transaction.atomic  #
    def create_run(self, request: Request, *args, **kwargs):
        token = request.data.get("token")
        task_type = request.data.get("task_type")
        hyperparameter = request.data.get("hyperparameter")
        # signature = request.data.get("signature")

        if not (token and task_type):
            return ErrorResponse(msg="token/task_type is required")

        try:
            sql_helper = SQLSearch()

            task_info = sql_helper.search(
                str_sql=f"select * from prosafeAI_modelV_task WHERE token='{token}';"
            )

            if not task_info:
                return ErrorResponse(msg="token is error")

            task_info = task_info[0]
            task_id = task_info["id"]
            if task_info["task_type"] == TASK_TYPE[task_type]:
                used_quantity = sql_helper.search(
                    str_sql=f"SELECT count(*) as count from prosafeAI_modelV_run WHERE task_id={task_id};"
                )[0]["count"]
                total_quantity = sql_helper.search(
                    str_sql=f"""SELECT total_quantity from prosafeAI_modelV_token_recharge
                        WHERE task_id={task_id} ORDER BY create_time DESC LIMIT 1;"""
                )[0]["total_quantity"]

                surplus_quantity = total_quantity - used_quantity

                if surplus_quantity:
                    hyperparameter = (
                        hyperparameter
                        if hyperparameter
                        else task_info["init_hyperparameter"]
                    )
                    run_id = sql_helper.insert(
                        str_sql=f"""insert into prosafeAI_modelV_run (task_type, hyperparameter, start_time, task_id) 
                        values ("{task_info['task_type']}", "{hyperparameter}", "{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", "{task_id}");"""
                    )

                    if used_quantity == 0:
                        sql_helper.update(
                            str_sql=f"""UPDATE prosafeAI_modelV_task SET status=1 WHERE id={task_id};"""
                        )

                    return DetailResponse(msg="success", data={"run_id": run_id})
                else:
                    return ErrorResponse(
                        msg="The token quantity has been used up，please recharge"
                    )
            else:
                return ErrorResponse(msg="task_type is error")

        except Exception as e:
            return ErrorResponse(e.__str__())

    @action(methods=["post"], detail=False)
    def check_metadata(self, request: Request, *args, **kwargs):
        token = request.data.get("token")
        run_id = request.data.get("run_id")
        file = request.FILES.get("file")
        # signature = request.data.get("signature")

        if not (token and run_id and file):
            return ErrorResponse(msg="token/run_id/file is required")

        try:
            sql_helper = SQLSearch()

            task_info = sql_helper.search(
                str_sql=f"""SELECT a.id, b.table_name_mysql, a.version from prosafeAI_modelV_task as a JOIN prosafeAI_table as b 
                on a.table_id=b.id WHERE token='{token}';
                """
            )
            if not task_info:
                return ErrorResponse(msg="token is error")

            task_id, table_name, version = (
                task_info[0]["id"],
                task_info[0]["table_name_mysql"],
                task_info[0]["version"],
            )

            metadata_set = set(
                [
                    results["image_name"]
                    for results in sql_helper.search(
                        str_sql=f"SELECT image_name from {table_name} WHERE data_version={version};"
                    )
                ]
            )

            check_result = []
            status = "PASS"
            for line in file.readlines():
                line = os.path.basename(line.decode().strip())
                if line in metadata_set:
                    check_result.append(",".join([line, "1"]))
                else:
                    check_result.append(",".join([line, "0"]))
                    status = "FAILED"

            date_time = datetime.datetime.now()

            root_path = os.path.join(
                "/data", "check_report", str(date_time.year), str(date_time.month)
            )
            if not os.path.isdir(root_path):
                os.makedirs(root_path)

            report_path = os.path.join(
                root_path,
                f"{table_name}_{version}_{date_time.strftime('%Y-%m-%d_%H:%M:%S')}.txt",
            )

            with open(report_path, "w", encoding="utf-8") as fw:
                fw.write("\n".join(check_result) + "\n")

            sql_helper.insert(
                str_sql=f"""insert into prosafeAI_modelV_check_report (report_path, status, create_time, run_id, task_id)
                              values ("{report_path}", "{status}", "{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
                              "{run_id}", "{task_id}")"""
            )

            if status == "PASS":
                return DetailResponse(msg="success")
            else:
                return ErrorResponse(msg="failed")

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["post"], detail=False)
    def get_ground_truth(self, request: Request, *args, **kwargs):
        # get object_detection annotation

        token = request.data.get("token")
        img_list = request.data.get("img_list", [])

        if not (token and img_list):
            return ErrorResponse(msg="token/img_list is required")

        try:
            sql_helper = SQLSearch()

            task_info = sql_helper.search(
                str_sql=f"""SELECT b.id, b.table_name_mysql, a.version, a.raw_hyperparameter from prosafeAI_modelV_task as a 
                JOIN prosafeAI_table as b 
                on a.table_id=b.id WHERE token='{token}';
                """
            )
            if not task_info:
                return ErrorResponse(msg="token is error")

            task_info = task_info[0]

            str_sql = f"SELECT table_name_mysql from prosafeAI_table where parent_id={task_info['id']} "
            where1 = 'and table_type="object"'
            where2 = 'and table_type="tag"'

            object_table_name = sql_helper.search(str_sql + where1)[0][
                "table_name_mysql"
            ]

            tag_table_name = sql_helper.search(str_sql + where2)[0]["table_name_mysql"]

            object_info = sql_helper.search(
                str_sql=f"""SELECT a.image_name, b.object_class, c.content from {task_info["table_name_mysql"]} a 
                JOIN {object_table_name} b on a.id=b.metadata_sample_id
                JOIN {tag_table_name} c on b.id=c.object_id 
                WHERE b.data_version={task_info["version"]} and c.feature like '%bbox%' and a.image_name in {tuple(img_list)};"""
            )

            results = {}

            for sub in object_info:
                results.setdefault(sub["image_name"], []).append(
                    {
                        "bbox": eval(sub["content"]),
                        "class": sub["object_class"],
                        "bbox_type": BBOX_TYPE[
                            eval(task_info["raw_hyperparameter"])["bbox_type"]
                        ],
                        "scale": eval(task_info["raw_hyperparameter"])["scale"],
                    }
                )

            return DetailResponse(data=results)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["post"], detail=False)
    @transaction.atomic
    def save_phased_results(self, request: Request, *args, **kwargs):
        token = request.data.get("token")
        run_id = request.data.get("run_id")
        results = request.data.get("results")
        status = request.data.get("status")
        # signature = request.data.get("signature")

        if not (token and run_id and results):
            return ErrorResponse(msg="token/run_id/results is required")

        try:
            sql_helper = SQLSearch()

            task_info = sql_helper.search(
                str_sql=f"select * from prosafeAI_modelV_task WHERE token='{token}';"
            )
            if not task_info:
                return ErrorResponse(msg="token is error")

            task_id = task_info[0]["id"]

            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sql_helper.insert(
                str_sql=f"""insert into prosafeAI_modelV_step (criteria, iteration, fail_test_num, total_mutator, ASR,
                 process_rate, running_time, ETA, status, create_time, run_id, task_id) values ("{results['criteria']}", 
                 "{results['iteration']}", "{results['fail_test_num']}", "{results['total_mutator']}", "{results['ASR']}", 
                 "{results['process_rate']}",  "{results['running_time']}", "{results['ETA']}", "{status}", 
                 "{create_time}", "{run_id}", "{task_id}");
            """
            )

            return DetailResponse(msg="success")

        except Exception as e:
            return ErrorResponse(msg=e.__str__())

    @action(methods=["post"], detail=False)
    @transaction.atomic  #
    def save_results(self, request: Request, *args, **kwargs):
        token = request.data.get("token")
        run_id = request.data.get("run_id")
        file = request.FILES.get("file")
        # signature = request.data.get("signature")

        if not (token and run_id and file):
            return ErrorResponse(msg="token/run_id/file is required")

        try:
            sql_helper = SQLSearch()

            task_info = sql_helper.search(
                str_sql=f"select * from prosafeAI_modelV_task WHERE token='{token}';"
            )
            if not task_info:
                return ErrorResponse(msg="token is error")

            date_time = datetime.datetime.now()

            root_path = os.path.join(
                "/data", "sdk_results", str(date_time.year), str(date_time.month)
            )
            if not os.path.isdir(root_path):
                os.makedirs(root_path)
            file_name, file_type = file.name.split(".")
            result_path = os.path.join(
                root_path,
                f'{file_name}-{date_time.strftime("%Y-%m-%d_%H:%M:%S")}.{file_type}',
            )

            with open(result_path, "wb") as fw:
                fw.write(file.read())

            task_info = task_info[0]

            tasks.__dict__[
                f"{task_info['task_type']}_{task_info['algorithm_type']}"
            ].delay(
                run_id=run_id,
                table_id=task_info["table_id"],
                version=task_info["version"],
                result_path=result_path,
                hyperparameter=task_info["init_hyperparameter"],
            )

            return DetailResponse(msg="success")

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
