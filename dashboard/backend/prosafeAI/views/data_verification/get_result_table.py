# -*- coding: utf-8 -*-
# @Time    : 2023/3/1 上午10:33
# @Author  : xiaxi
# @File    : get_result_table.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.views import APIView


class ResultTableView(APIView):
    def get(self, request):
        task_id = request.query_params.get("id")

        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        if not task_id:
            return ErrorResponse(msg="task_id is required")

        try:
            sql_helper = SQLSearch()

            str_sql = f"""
                SELECT A.`requirements_id`, A.`rule_id`, A.`rule_name`, A.`classification`, A.`verification_object`, A.`verification_content`, A.`computation_rule`, B.`test_result` 
                FROM prosafeAI_data_sub_requirements A
                    LEFT JOIN prosafeAI_data_verification_result B ON A.requirements_id=B.requirements_id and A.id=B.sub_requirements_id
                WHERE B.task_id={task_id}
            """

            data = sql_helper.search(str_sql)
            total = len(data)
            start = (page - 1) * limit
            # data = data[start: start + limit]

            return SuccessResponse(
                data=data[start : start + limit], limit=limit, page=page, total=total
            )

        except Exception as e:
            return ErrorResponse(e.__str__())
