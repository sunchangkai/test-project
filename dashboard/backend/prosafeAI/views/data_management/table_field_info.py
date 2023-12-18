# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 下午4:04
# @Author  : liuliping
# @File    : table_field_info.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.views import APIView


class FieldInfoView(APIView):
    def get(self, request):
        table_id = request.query_params.get("table_id")
        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        if not table_id:
            return ErrorResponse(msg="table_id is required")

        try:
            sql_helper = SQLSearch()

            data = sql_helper.search(
                f"SELECT field_name FROM prosafeAI_field  where table_id={table_id} AND field_category != '';"
            )

            return SuccessResponse(data=data, page=page, limit=limit, total=len(data))

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
