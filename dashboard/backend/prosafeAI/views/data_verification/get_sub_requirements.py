# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 下午7:30
# @Author  : xiaxi
# @File    : get_sub_requirements.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.views import APIView


class SubRequirementsTableView(APIView):
    def get(self, request):
        requirements_id = request.query_params.get("id")

        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        if not requirements_id:
            return ErrorResponse(msg="requirements_id is required")

        try:
            sql_helper = SQLSearch()

            str_sql = f"""
                SELECT `rule_id`, `rule_name`, `classification`, `verification_object`, `verification_content`, `computation_rule`
                FROM prosafeAI_data_sub_requirements
                WHERE requirements_id = {requirements_id}
                ORDER by id
            """

            data = sql_helper.search(str_sql)
            total = len(data)
            start = (page - 1) * limit
            # data = data[start: start + limit]

            return SuccessResponse(
                data=data[start : start + limit], limit=limit, page=page, total=total
            )

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
