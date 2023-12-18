# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 上午10:33
# @Author  : liuliping
# @File    : table_details.py
# @description:

from django.db import connection
from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView


class TableDetailsView(APIView):
    def get(self, request):
        version = request.query_params.get("version")
        table_id = request.query_params.get("table_id")
        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))
        search_param = request.query_params.get("search_param")
        search_content = request.query_params.get("search_content")
        search_type = request.query_params.get("search_type", "0")

        if not table_id:
            return ErrorResponse(msg="table_id is required")

        try:
            sql_helper = SQLSearch()

            table_name = sql_helper.search(
                f"SELECT table_name_mysql FROM prosafeAI_table where id={table_id};"
            )[0]["table_name_mysql"]

            latest_version = sql_helper.search(
                f"SELECT max(version) as latest FROM prosafeAI_version where table_id={table_id};"
            )[0]["latest"]

            version = version if version else latest_version

            if search_param:
                if search_type == "0":
                    where = f'and {search_param}="{search_content}"'
                else:
                    where = f'and {search_param} like "%{search_content}%"'
            else:
                where = ""

            str_sql1 = f"""SELECT count(*) as total from {table_name} WHERE data_version={version} {where};"""

            total = sql_helper.search(str_sql1)[0]["total"]

            start = (page - 1) * limit

            str_sql2 = f"""SELECT * from {table_name} WHERE data_version={version} {where} limit {start}, {limit};"""

            data = sql_helper.search(str_sql2)

            object_table_name = sql_helper.search(
                f"""SELECT table_name_mysql from prosafeAI_table 
                                                                  where parent_id={table_id} and table_type='object';"""
            )

            if object_table_name:
                object_table_name = object_table_name[0]["table_name_mysql"]

            for sub in data:
                if object_table_name:
                    object_num = sql_helper.search(
                        f"""SELECT count(object_class) as num from {object_table_name} 
                                    WHERE metadata_table_id={table_id} and data_version={version} and metadata_sample_id={sub["id"]};"""
                    )

                    sub["object_num"] = object_num[0]["num"]

                else:
                    sub["object_num"] = 0

            return SuccessResponse(data=data, page=page, limit=limit, total=total)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
