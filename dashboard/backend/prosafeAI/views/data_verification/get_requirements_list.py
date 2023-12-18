# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 下午3:57
# @Author  : xiaxi
# @File    : get_requirements_table.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from rest_framework.views import APIView


class RequirementsTableView(APIView):
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
                    where = f" WHERE usercase_id in ({usercase_ids})"

                else:
                    return SuccessResponse(data=[])

            else:
                where = ""

            str_sql = f"""
                SELECT `id`, `name`, DATE_FORMAT(`create_time`, '%m/%d/%Y %H:%i:%s') as create_time
                FROM prosafeAI_data_requirements
                {where}
                ORDER BY create_time DESC
            """

            data = sql_helper.search(str_sql)
            total = len(data)
            start = (page - 1) * limit

            return SuccessResponse(
                data=data[start : start + limit], limit=limit, page=page, total=total
            )

        except Exception as e:
            return ErrorResponse(e.__str__())
