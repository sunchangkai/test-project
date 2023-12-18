# -*- coding: utf-8 -*-
# @Time    : 2023/3/8 17:17
# @Author  : xiaxi
# @File    : run_verification.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
import json
from scipy.stats import chi2_contingency

# from scipy.stats import chi2
import datetime


METHOD_DICT = {
    ("dataset", "scenario coverage"): "type_1",
    ("dataset", "scenario coverage by scenario catalogue"): "type_2",
    ("dataset", "parameter coverage"): "type_3",
    ("dataset", "distribution"): "type_4",
    ("dataset", "amount"): "type_5",
    ("dataset", "label balance"): "type_6",
    ("image", "quality"): "type_7",
    ("image", "annotation"): "type_8",
    ("image", "perspective"): "type_9",
    ("bounding box", "object count"): "type_10",
    ("bounding box", "visibility"): "type_11",
    ("bounding box", "deviation"): "type_12",
    ("meta data", "schema"): "type_13",
    ("meta data", "odd information"): "type_14",
    ("meta data", "mapping"): "type_15",
    ("class label", "taxonomy"): "type_16",
    ("class label", "specification"): "type_17",
}


class RunVerificationViewSet(ViewSet):
    @action(methods=["post"], detail=False)
    def run_verification(self, request: Request, *args, **kwargs):
        task_id = request.data.get("task_id")

        if not task_id:
            return ErrorResponse(msg="task_id is required")

        try:
            test_begin_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            data, metadata_table, version, field_list, total_amount = get_info_from_sql(
                task_or_subtask="task_id", id=task_id
            )
            numbers = len(data)

            msg_all = {}

            for item in range(numbers):
                subtask = data[item]

                result, Reason = run_test_by_model_type(
                    subtask, metadata_table, version, field_list, total_amount
                )
                msg_all[subtask["rule_name"]] = result

            # update status for task
            test_end_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            msg_task = update_task_status(task_id, test_begin_time, test_end_time)
            msg_all["task"] = str(msg_task)

            msg = str("data verification success")
            return DetailResponse(msg=msg)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())


def get_info_from_sql(task_or_subtask, id):
    sql_helper = SQLSearch()
    str_sql = f"""
        SELECT B.`id`, B.`task_id`, A.`requirements_id`, A.`rule_id`, A.`rule_name`, A.`classification`, A.`verification_object`, A.`verification_content`, A.`computation_rule`, B.`test_result` , C.`table_name_mysql`, B.`version`, B.`table_id`
        FROM prosafeAI_data_sub_requirements A
        INNER JOIN prosafeAI_data_verification_result B ON A.requirements_id=B.requirements_id and A.id=B.sub_requirements_id
        INNER JOIN prosafeAI_table C ON B.`table_id`= C.`id`
        WHERE B.{task_or_subtask}={id};
    """
    # print(str_sql)
    data = sql_helper.search(str_sql)

    table_id = data[0]["table_id"]
    metadata_table = data[0]["table_name_mysql"]
    version = data[0]["version"]

    sql_field = f"""SELECT field_name from prosafeAI_field WHERE table_id={table_id}"""
    field_data = sql_helper.search(sql_field)
    field_list = [field_data[item]["field_name"] for item in range(len(field_data))]

    sql_total = f"""SELECT count(*) as count FROM {metadata_table} WHERE data_version={version}"""
    total_amount = sql_helper.search(sql_total)[0]["count"]
    return data, metadata_table, version, field_list, total_amount


def run_test_by_model_type(subtask, metadata_table, version, field_list, total_amount):
    sql_helper = SQLSearch()

    subtask_id = subtask["id"]

    verification_object = subtask["verification_object"]
    verification_content = subtask["verification_content"]
    computation_rule = json.loads(subtask["computation_rule"])
    key = (verification_object, verification_content)
    model_type = METHOD_DICT[key]

    if model_type == "type_1":
        operator = computation_rule["operator"]
        threshold = computation_rule["threshold"]
        scenarios = computation_rule["scenario"]
        number_scenario = len(scenarios)

        sql_count = f""" SELECT count(*) as count FROM {metadata_table} WHERE data_version={version}"""

        Flag = True
        Reason = f"""From the metadata, can not find odd_parameter: """

        for scenario_item in range(number_scenario):
            odd_parameter = scenarios[scenario_item]["odd_parameter"]
            if odd_parameter not in field_list:
                Flag = False
                Reason += f"""{odd_parameter},"""

        if Flag is False:
            result = "REJECTED"
            Reason = Reason.rstrip(",") + "."

        else:
            for scenario_item in range(number_scenario):
                odd_parameter = scenarios[scenario_item]["odd_parameter"]
                odd_class = str(scenarios[scenario_item]["odd_class"])
                sql_slice = f""" AND {odd_parameter} like '{odd_class}%'"""
                sql_count += sql_slice

            counts = sql_helper.search(sql_count)[0]["count"]
            rule = str(counts) + operator + str(threshold)
            if eval(rule):
                result = "PASSED"
            else:
                result = "FAILED"
            Reason = "No error."

    elif model_type == "type_3":
        odd_parameter = computation_rule["odd_parameter"]
        if odd_parameter in field_list:
            sql_type_3 = f""" SELECT count(*) as count FROM {metadata_table} WHERE data_version={version} AND `{odd_parameter}` is NULL """
            counts_type_3 = sql_helper.search(sql_type_3)[0]["count"]
            if counts_type_3 == 0:
                result = "PASSED"
            else:
                result = "FAILED"
            Reason = "No error."
        else:
            result = "REJECTED"
            Reason = f"""Can not find odd_parameter: {odd_parameter} in the metadata."""

    elif model_type == "type_4":
        odd_parameter = computation_rule["odd_parameter"]
        if odd_parameter in field_list:
            statistical_distribution = computation_rule[
                "statistical_distribution"
            ]  # a list
            statistical_test = computation_rule["statistical_test"]
            significance = computation_rule["significance"]
            if statistical_test == "Chi Square Test":
                odd_class_list = [
                    statistical_distribution[item]["odd_class"]
                    for item in range(len(statistical_distribution))
                ]
                probability = [
                    statistical_distribution[item]["probability"]
                    for item in range(len(statistical_distribution))
                ]
                frequency_test = list(map(lambda x: x * total_amount, probability))

                # amount
                sql_type_4 = f"""SELECT {odd_parameter}, count(id) as count FROM {metadata_table} WHERE data_version={version} GROUP BY {odd_parameter};"""
                counts_type_4 = sql_helper.search(sql_type_4)
                odd_class_dict = {}
                frequency_dict = {}
                for item in range(len(counts_type_4)):
                    odd_class_dict[counts_type_4[item][odd_parameter]] = counts_type_4[
                        item
                    ]["count"]

                for item_odd in range(len(odd_class_list)):
                    odd_name = odd_class_list[item_odd]
                    if odd_name in odd_class_dict.keys():
                        frequency_dict[odd_name] = odd_class_dict[odd_name]
                    else:
                        frequency_dict[odd_name] = 0

                frequency_real = list(frequency_dict.values())

                table = [frequency_test, frequency_real]
                stat, p, freedom_degrees, expected = chi2_contingency(
                    table, correction=False
                )
                if p < significance:
                    result = "FAILED"
                else:
                    result = "PASSED"
                Reason = "No error."

            else:
                result = "REJECTED"
                Reason = f"""The type of distribution test: '{statistical_test}' is not supported at the moment. Currently, only 'Chi Square Test' is supported."""

        else:
            result = "REJECTED"
            Reason = (
                f"""Can not find odd_parameter: '{odd_parameter}' in the metadata."""
            )

    elif model_type == "type_5":
        if computation_rule["metric"] == "total amount":
            rule = (
                str(total_amount)
                + computation_rule["operator"]
                + str(computation_rule["threshold"])
            )
            if eval(rule):
                result = "PASSED"
            else:
                result = "FAILED"
            Reason = "No error."
        else:
            result = "REJECTED"
            Reason = f"""The type of metric: '{computation_rule["metric"]}' is not supported at the moment. Currently, only 'total amount' is supported. """

    else:
        result = "SKIP"
        Reason = "NULL"

    str_sql_reason = f"""UPDATE prosafeAI_data_verification_result SET `test_result`="{result}", `result_description`="{Reason}" WHERE `id`={subtask_id};"""
    sql_helper.update(str_sql=str_sql_reason)
    # print(str_sql_reason)
    return result, Reason


def update_task_status(task_id, test_begin_time, test_end_time):
    sql_helper = SQLSearch()

    sql_helper.update(
        str_sql=f"""UPDATE prosafeAI_data_verification_task SET `status`="DONE", `test_begin_time`=STR_TO_DATE('{test_begin_time}', '%Y-%m-%d %H:%i:%s'), `test_end_time`=STR_TO_DATE('{test_end_time}', '%Y-%m-%d %H:%i:%s') WHERE `id`={task_id};"""
    )
    return "DONE"
