# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 下午2:44
# @Author  : liuliping
# @File    : data_statistics.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse, ErrorResponse


class DataStatisticsViewSet(ViewSet):
    @action(methods=["post"], detail=False)
    def data_statistics(self, request: Request, *args, **kwargs):
        table_id = request.data.get("table_id")
        table_name = request.data.get("table_name")
        count_type = request.data.get("count_type", 0)
        fields = request.data.get("fields", [])
        versions = request.data.get("versions", [])

        if not (table_name or table_id):
            return ErrorResponse(msg="must have table_info")

        if not fields:
            return ErrorResponse(msg="please choose fields")

        if not versions:
            where = f"SELECT max(version) as latest FROM prosafeAI_version WHERE table_id={table_id}"

        else:
            where = ",".join(str(version) for version in versions)

        try:
            sql_helper = SQLSearch()

            results = []

            for field in fields:
                if count_type == 0:  # sample count
                    str_sql = f"""
                    SELECT {field}, data_version, COUNT(*) as count from {table_name} WHERE data_version in 
                    ({where}) GROUP BY {field}, data_version;
                    """

                else:  # object count
                    object_table_name = sql_helper.search(
                        f"""
                    SELECT table_name_mysql from prosafeAI_table where parent_id={table_id} and table_type="object"
                    """
                    )

                    object_table_name = object_table_name[0]["table_name_mysql"]

                    str_sql = f"""
                    SELECT a.{field}, a.data_version, COUNT(b.id) as count from {table_name} as a 
                    JOIN {object_table_name} as b on  a.id=b.metadata_sample_id
                    WHERE a.data_version in ({where}) GROUP BY a.{field}, a.data_version; 
                    """

                data = sql_helper.search(str_sql)

                tmp = {"odd_name": field}

                for sub in data:
                    tmp.setdefault("detail", []).append(
                        {
                            "data_version": int(sub["data_version"]),
                            "odd_value": sub[field],
                            "count": sub["count"],
                        }
                    )
                results.append(tmp)

            return DetailResponse(data=results)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
