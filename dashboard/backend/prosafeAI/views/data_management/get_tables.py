# -*- coding: utf-8 -*-
# @Time    : 2023/2/13 上午11:45
# @Author  : liuliping
# @File    : get_tables.py
# @description:

from django.db import connection
from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView


class TablesView(APIView):
    # @action(methods=['GET'], detail=False, permission_classes=[])
    def get(self, request):
        user = request.user

        limit = int(request.query_params.get("limit", 100))
        page = int(request.query_params.get("page", 1))

        try:
            sql_helper = SQLSearch()

            if not user.is_superuser:
                usercase_ids = sql_helper.search(
                    f"SELECT usercase_id from prosafeAI_usercase_member WHERE user_id={user.id}"
                )
                usercase_ids = ",".join(
                    [str(usercase["usercase_id"]) for usercase in usercase_ids]
                )

                if usercase_ids:
                    where = f"AND b.id in ({usercase_ids})"

                else:
                    return SuccessResponse(data=[])

            else:
                where = ""

            str_sql = f"""
                SELECT c.*, a.`name` AS project_name, b.`name` AS usercase_name 
                FROM prosafeAI_project as a 
                    JOIN prosafeAI_usercase as b ON a.id=b.project_id 
                    JOIN prosafeAI_table as c ON b.id=c.usercase_id
                WHERE c.table_type='metadata' {where};
            """
            data = sql_helper.search(str_sql)
            total = len(data)
            start = (page - 1) * limit
            data = data[start : start + limit]
            for sub in data:
                latest_version = sql_helper.search(
                    f'SELECT max(version) as latest FROM prosafeAI_version WHERE table_id={sub["id"]};'
                )

                sub["latest_version"] = latest_version[0]["latest"]

                fields = sql_helper.search(
                    f'SELECT field_name FROM prosafeAI_field WHERE table_id={sub["id"]};'
                )

                sub["fields"] = [field["field_name"] for field in fields]

                object_table_name = sql_helper.search(
                    f"""SELECT table_name_mysql FROM prosafeAI_table 
                                              WHERE parent_id='{sub["id"]}' AND table_type='object';"""
                )

                if object_table_name:
                    object_table_name = object_table_name[0]["table_name_mysql"]
                    object_num = sql_helper.search(
                        f"""SELECT count(object_class) as num FROM {object_table_name} 
                    WHERE metadata_table_id={sub["id"]} AND data_version={sub["latest_version"]};"""
                    )

                    sub["object_num"] = object_num[0]["num"]
                    sub["task_type"] = 1

                else:
                    sub["object_num"] = 0
                    sub["task_type"] = 0

            return SuccessResponse(data=data, limit=limit, page=page, total=total)

        except Exception as e:
            return ErrorResponse(msg=e.__str__())


# if __name__ == '__main__':
# sql_helper = SQLSearch()
#
# search_res = sql_helper.search("select field_name, field_type from prosafeAI_field")
#
# insert_res = sql_helper.insert("insert into prosafeAI_field (field_name, field_type, odd_id, table_id) "
#                                "values ('abc', 'feature', '4', '1'), ('defg', 'odd', '4', '1')")
#
# update_res = sql_helper.update("update prosafeAI_field set field_name='vvvv' where field_name='abc'")
#
# delete_res = sql_helper.delete("delete from prosafeAI_field where field_name='vvvv'")

# get_tables(request=None)
