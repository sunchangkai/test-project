# -*- coding: utf-8 -*-
# @Time    : 2023/3/12 17:17
# @Author  : xiaxi
# @File    : run_subtask.py
# @description:


from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request

from prosafeAI.views.data_verification.run_verification import (
    get_info_from_sql,
    run_test_by_model_type,
    update_task_status,
)


class RunSubTaskViewSet(ViewSet):
    @action(methods=["post"], detail=False)
    def run_for_subtask(self, request: Request, *args, **kwargs):
        subtask_id = request.data.get("subtask_id")

        if not subtask_id:
            return ErrorResponse(msg="subtask_id is required")

        try:
            data, metadata_table, version, field_list, total_amount = get_info_from_sql(
                task_or_subtask="id", id=subtask_id
            )

            subtask = data[0]
            msg_all = {}
            result, Reason = run_test_by_model_type(
                subtask, metadata_table, version, field_list, total_amount
            )
            msg_all[subtask["rule_name"]] = f""" {result} . """

            # msg_task = update_task_status(subtask['task_id'])
            # msg_all["task"] = str(msg_task)

            msg = str("subtask success")

            return DetailResponse(msg=msg)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
