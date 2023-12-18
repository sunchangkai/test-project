# -*- coding: utf-8 -*-
# @Time    : 2023/3/1 上午11:45
# @Author  : xiaxi
# @File    : get_task_table.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.views import APIView


class TaskTableView(APIView):
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
                    where = f"AND A.usercase_id in ({usercase_ids})"

                else:
                    return SuccessResponse(data=[])

            else:
                where = ""

            str_sql = f"""
                SELECT B.`id`, B.`task_name`, C.`table_description`, B.`version`, A.`name` AS requirements, 
                DATE_FORMAT(B.`test_begin_time`, '%m/%d/%Y %H:%i:%s') as test_begin_time, 
                DATE_FORMAT(B.`test_end_time`, '%m/%d/%Y %H:%i:%s') as test_end_time, 
                B.`status`, B.`requirements_id`
                FROM prosafeAI_data_verification_task B
                    INNER JOIN prosafeAI_data_requirements A ON A.id=B.requirements_id
                    INNER JOIN prosafeAI_table C ON C.id=B.table_id
                WHERE C.table_type='metadata' {where}
                ORDER BY B.id DESC
            """

            data = sql_helper.search(str_sql)
            total = len(data)
            start = (page - 1) * limit

            return SuccessResponse(
                data=data[start : start + limit], limit=limit, page=page, total=total
            )

        except Exception as e:
            return ErrorResponse(msg=e.__str__())
