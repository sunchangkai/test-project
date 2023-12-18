# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 下午1:20
# @Author  : liuliping
# @File    : table_version_info.py
# @description:

from django.db import connection
from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
import datetime


class VersionInfoView(APIView):
    def get(self, request):
        table_id = request.query_params.get("table_id")
        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        if not table_id:
            return ErrorResponse(msg="table_id is required")

        try:
            sql_helper = SQLSearch()

            data = sql_helper.search(
                f"""SELECT version, description, DATE_FORMAT(create_time, '%m/%d/%Y %H:%i:%s') as create_time FROM prosafeAI_version where table_id={table_id} 
                ORDER BY version DESC
                """
            )

            total = len(data)
            start = (page - 1) * limit

            # for sub in data:
            #     time = sub["create_time"]
            #     sub["create_time"] = time.strftime('%m/%d/%Y %H:%M:%S')

            return SuccessResponse(
                data=data[start : start + limit], page=page, limit=limit, total=total
            )

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
