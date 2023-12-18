# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 9:09
# @Author  : xiaxi
# @File    : import_task.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from django.http import HttpResponse
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from prosafeAI.views.data_verification.manager import DataRequirementsManager
from django.conf import settings
from urllib.parse import quote


import json
import os
import datetime


class ImportTaskViewSet(ViewSet):
    @action(methods=["get", "post"], detail=False)
    def import_task(self, request: Request, *args, **kwargs):
        # export data_requirements.json template
        if request.method == "GET":
            try:
                data = {
                    "requirements_catalog": {
                        "name": "string",
                        "id": "string",
                        "requirements": [
                            {
                                "name": "string",
                                "id": "string",
                                "type": "string",
                                "classification": "string",
                                "export": "string",
                                "description": {
                                    "verification_object": "string",
                                    "verification_content": "string",
                                    "computation_rule": {},
                                },
                            },
                        ],
                    },
                }

                response = HttpResponse(content_type="application/json;charset=utf-8")

                response["Access-Control-Expose-Headers"] = f"Content-Disposition"
                response[
                    "Content-Disposition"
                ] = f'attachment;filename={quote(f"export_data_requirements_json_template.json")}'
                response.write(json.dumps([data], indent=4))

                return response

            except Exception as e:
                return ErrorResponse(msg=e.__str__())

        table_id = int(request.data.get("table"))
        version = int(request.data.get("table_version"))
        requirements_id = int(request.data.get("requirement"))
        task_name = request.data.get("task_name")

        if not table_id or not version or not requirements_id or not task_name:
            return ErrorResponse(
                msg="table_id/version/requirements_id/task_name is required"
            )

        if requirements_id < 1:  # -1 import new json
            # get new json from url
            file_url = request.data.get("json_url")

            if not file_url:
                return ErrorResponse(msg="file_url is required")

            #
            file_path_dir = os.path.join(settings.BASE_DIR, file_url)

            try:
                manager = DataRequirementsManager()
                data_requirements_catalog = manager.read_requirements(
                    file_path_dir
                )  # pass sanity_checks
                requirements_result = create_requirements(
                    data_requirements_catalog, table_id
                )
                # update data_verification_task & data_verification_result
                if requirements_result[1]:
                    requirements_id = requirements_result[1]
                    task_result = create_task(
                        table_id, version, requirements_id, task_name
                    )
                    os.remove(file_path_dir)

                    # return DetailResponse(msg=task_result) if "success" in msg else ErrorResponse(msg=msg)

                    if "success" in task_result[0]:
                        return DetailResponse(
                            msg=task_result[0], data={"task_id": task_result[1]}
                        )
                    else:
                        return ErrorResponse(msg=task_result[0])

                else:
                    msg = requirements_result[0]
                    return ErrorResponse(msg=msg)

            except Exception as e:
                return ErrorResponse(msg=e.__str__())

        else:  # requirements_id >= 1
            # update data_verification_task & data_verification_result
            msg = create_task(table_id, version, requirements_id, task_name)

        return DetailResponse(msg=msg) if "success" in msg else ErrorResponse(msg=msg)


def create_requirements(data_requirements_catalog, table_id):
    try:
        sql_helper = SQLSearch()
        usercase_id = sql_helper.search(
            f"""SELECT usercase_id FROM prosafeAI_table where id={table_id} 
                """
        )[0]["usercase_id"]

        requirements = data_requirements_catalog["requirements_catalog"]["requirements"]
        numbers = len(requirements)

        name = data_requirements_catalog["requirements_catalog"]["name"]
        content = json.dumps(data_requirements_catalog)

        requiremenst_data = (
            str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            str(name),
            content,
            int(usercase_id),
        )
        # update data_requirements
        requirements_id = sql_helper.insert(
            str_sql=f"""insert into prosafeAI_data_requirements (create_time, name, content, usercase_id) 
        values {requiremenst_data};"""
        )

        # search for requirements_id
        # requirements_id = int(sql_helper.search(f"""SELECT max(id) as id FROM prosafeAI_data_requirements where usercase_id={usercase_id}""")[0]["id"])

        # update data_sub_requirements
        data = [
            (
                requirements_id,
                str(requirements[item]["id"]),
                str(requirements[item]["name"]),
                str(requirements[item]["classification"]),
                str(requirements[item]["description"]["verification_object"]),
                str(requirements[item]["description"]["verification_content"]),
                json.dumps(
                    requirements[item]["description"]["computation_rule"], indent=4
                ),
            )
            for item in range(numbers)
        ]

        sql_helper.insertmany(
            str_sql=f"""INSERT INTO prosafeAI_data_sub_requirements (requirements_id, rule_id, rule_name, classification, verification_object, verification_content, computation_rule) VALUES (%s, %s, %s, %s, %s, %s, %s);""",
            values=data,
        )

        msg = ("import requirements success", requirements_id)
    except Exception as e:
        msg = (str(e), None)

    return msg


def create_task(table_id, version, requirements_id, task_name):
    try:
        sql_helper = SQLSearch()
        # update data_verification_task
        task_id = sql_helper.insert(
            str_sql=f"""insert into prosafeAI_data_verification_task (table_id, version, requirements_id, task_name, status) 
                    values ("{table_id}", "{version}", "{requirements_id}", "{task_name}", "PLAN");"""
        )

        #  search for task_id
        # task_id = sql_helper.search(f"""SELECT max(id) as id FROM prosafeAI_data_verification_task""")[0]["id"]

        # search for sub_requirements_id_list
        sub_requirements_id_list = sql_helper.search(
            f"""SELECT id FROM prosafeAI_data_sub_requirements where requirements_id={requirements_id}"""
        )

        length = len(sub_requirements_id_list)

        # update data_verification_result
        data = [
            (
                str(task_id),
                str(table_id),
                str(sub_requirements_id_list[item]["id"]),
                str(requirements_id),
                str(version),
            )
            for item in range(length)
        ]

        sql_helper.insertmany(
            str_sql=f"""INSERT INTO prosafeAI_data_verification_result (task_id, table_id, sub_requirements_id, requirements_id, version) VALUES (%s, %s, %s, %s, %s);""",
            values=data,
        )

        msg = ("import task success", task_id)

    except Exception as e:
        msg = (str(e), None)

    return msg
