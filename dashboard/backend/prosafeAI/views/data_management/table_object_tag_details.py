# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 下午5:20
# @Author  : liuliping
# @File    : table_object_tag_details.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.views import APIView


class TableObjectTagDetailsView(APIView):
    def get(self, request):
        version = request.query_params.get("version")
        table_id = request.query_params.get("table_id")
        sample_id = request.query_params.get("sample_id")
        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        if not table_id or not version or not sample_id:
            return ErrorResponse(msg="table_id/version/sample_id is required")

        try:
            sql_helper = SQLSearch()

            # get table name
            str_sql = f"SELECT table_name_mysql from prosafeAI_table where parent_id={table_id} "
            where1 = 'and table_type="object"'
            where2 = 'and table_type="tag"'
            object_table_name = sql_helper.search(str_sql + where1)

            object_table_name = object_table_name[0]["table_name_mysql"]

            tag_table_name = sql_helper.search(str_sql + where2)

            tag_table_name = tag_table_name[0]["table_name_mysql"]

            object_data = sql_helper.search(
                f"""SELECT id, object_class, object_code from {object_table_name}
                            WHERE metadata_table_id={table_id} and data_version={version} and metadata_sample_id={sample_id}
    --                         limit {(page - 1) * limit}, {limit};
                            """
            )

            data = []
            total = len(object_data)
            start = (page - 1) * limit

            for sub in object_data[start : start + limit]:
                object_id = sub["id"]

                object_tag = sql_helper.search(
                    f"""SELECT feature, content FROM {tag_table_name} where object_id={object_id};"""
                )

                data.append(
                    {
                        "object_id": sub["id"],
                        "object_class": sub["object_class"],
                        "object_code": sub["object_code"],
                        "object_tag": object_tag,
                    }
                )

            return SuccessResponse(data=data, limit=limit, page=page, total=total)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
