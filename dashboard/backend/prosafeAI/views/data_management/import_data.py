# -*- coding: utf-8 -*-
# @Time    : 2023/2/21 下午2:30
# @Author  : liuliping
# @File    : import_data.py
# @description:

from sql_helper.SQLSearch import SQLSearch
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from django.http import HttpResponse
import json
from urllib.parse import quote
from django.db import transaction
import os
from django.conf import settings
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
import datetime


# class ImportDataView(APIView):
class ImportDataViewSet(ViewSet):
    @action(methods=["get", "post"], detail=False)
    @transaction.atomic  # Django 事务,防止出错
    def import_data(self, request: Request, *args, **kwargs):
        # export template
        if request.method == "GET":
            table_id = request.query_params.get("table_id", 3)

            if not table_id:
                return ErrorResponse(msg="table_id is required")

            try:
                sql_helper = SQLSearch()
                table_fields = sql_helper.search(
                    f"SELECT field_name, field_type FROM prosafeAI_field where table_id={table_id};"
                )

                data = {sub["field_name"]: sub["field_type"] for sub in table_fields}

                object_table_name = sql_helper.search(
                    f"""SELECT table_name_mysql FROM prosafeAI_table 
                                                                  WHERE parent_id='{table_id}' AND table_type='object';"""
                )

                if object_table_name:
                    data["objects"] = [{"object_class": "string", "tag": {}}]

                response = HttpResponse(content_type="application/json;charset=utf-8")

                response["Access-Control-Expose-Headers"] = f"Content-Disposition"
                response[
                    "Content-Disposition"
                ] = f'attachment;filename={quote(f"export_json_template.json")}'
                response.write(json.dumps([data], indent=4))

                return response

            except Exception as e:
                return ErrorResponse(msg=e.__str__())

        # import data
        table_id = request.data.get("table_id")
        version_comments = request.data.get("version_comments")
        url = request.data.get("url")
        # label_map = request.data.get("label_map", {})
        label_file = request.FILES.get("label_file")

        if not table_id or not version_comments or not url:
            return ErrorResponse(
                msg="table_id/version_comments/url/label_file is required"
            )

        try:
            with label_file.open() as f:
                txt = f.read().decode("utf-8")

            label_map = {int(sub.split()[0]): sub.split()[1] for sub in txt.split("\n")}

            result = import_to_sql(table_id, version_comments, url, label_map)

            if "success" in result[0]:
                return DetailResponse(msg=result[0], data={"data_version": result[1]})
            else:
                return ErrorResponse(msg=result[0])

        except Exception as e:
            return ErrorResponse(msg=e.__str__())


def import_to_sql(table_id, version_comment, file_url, label_map):
    """
    read json file and load to Mysql
    :param file_url:
    :return:
    """
    # read json file
    file_path_dir = os.path.join(settings.BASE_DIR, file_url)

    with open(file_path_dir, encoding="utf-8") as fr:
        data = json.load(fr)

    sql_helper = SQLSearch()

    # get table name

    metadata_table_name = sql_helper.search(
        f"SELECT table_name_mysql from prosafeAI_table where id={table_id}"
    )
    metadata_table_name = metadata_table_name[0]["table_name_mysql"]

    object_table_name = None

    if data[0].get("objects"):  # if include objects
        str_sql = (
            f"SELECT table_name_mysql from prosafeAI_table where parent_id={table_id} "
        )
        where1 = 'and table_type="object"'
        where2 = 'and table_type="tag"'
        object_table_name = sql_helper.search(str_sql + where1)

        object_table_name = object_table_name[0]["table_name_mysql"]

        tag_table_name = sql_helper.search(str_sql + where2)

        tag_table_name = tag_table_name[0]["table_name_mysql"]

    latest_version = sql_helper.search(
        f"SELECT max(version) as latest FROM prosafeAI_version WHERE table_id={table_id};"
    )

    current_version = (
        latest_version[0]["latest"] + 1 if latest_version[0]["latest"] else 1
    )

    # initial version
    start_meta_id = 1
    start_object_id = 1

    if current_version != 1:
        latest_meta_id = sql_helper.search(
            f"SELECT max(id) as latest_meta FROM {metadata_table_name};"
        )

        start_meta_id = latest_meta_id[0]["latest_meta"] + 1

        if object_table_name:
            latest_object_id = sql_helper.search(
                f"SELECT max(id) as latest_object FROM {object_table_name};"
            )

            start_object_id = latest_object_id[0]["latest_object"] + 1

    meta_data, object_data, tag_data = [], [], []

    for idx_meta, sub_data in enumerate(data):
        tmp_meta = [str(start_meta_id + idx_meta), str(current_version)]

        for key, val in sub_data.items():
            if key == "objects":
                for idx_object, sub_object in enumerate(val):
                    tmp_object = [
                        str(start_object_id + idx_object),
                        str(table_id),
                        str(current_version),
                        str(start_meta_id + idx_meta),
                        str(sub_object["object_class"]),
                        str(sub_object["object_code"]),
                    ]

                    object_data.append("*&*".join(tmp_object))

                    for feature, content in sub_object["tag"].items():
                        tmp_tag = [
                            "",
                            str(table_id),
                            str(current_version),
                            str(start_meta_id + idx_meta),
                            str(start_object_id + idx_object),
                            feature,
                            str(content),
                        ]

                        tag_data.append("*&*".join(tmp_tag))

                start_object_id += len(val)

            else:
                tmp_meta.append(str(val))

        meta_data.append("*&*".join(tmp_meta))

    meta_path_dir = file_path_dir.replace(".json", "_meta.csv")

    with open(meta_path_dir, "w", encoding="utf-8") as fw:
        fw.write("\n".join(meta_data))

    res_meta = sql_helper.sql_load_bool(meta_path_dir, metadata_table_name)

    if object_table_name:
        object_path_dir = file_path_dir.replace(".json", "_object.csv")
        tag_path_dir = file_path_dir.replace(".json", "_tag.csv")

        with open(object_path_dir, "w", encoding="utf-8") as fw:
            fw.write("\n".join(object_data))

        with open(tag_path_dir, "w", encoding="utf-8") as fw:
            fw.write("\n".join(tag_data))

        res_object = sql_helper.sql_load_bool(object_path_dir, object_table_name)

        if res_object:
            os.remove(object_path_dir)

        res_tag = sql_helper.sql_load_bool(tag_path_dir, tag_table_name)

        if res_tag:
            os.remove(tag_path_dir)

    if res_meta:
        # if success, update version

        # label_map = {int(key): val for key, val in label_map.items()}

        sql_helper.insert(
            str_sql=f"""insert into prosafeAI_version (create_time, table_id, description, version, label_map) 
        values ("{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", "{table_id}", "{version_comment}", 
        "{current_version}", "{label_map}");"""
        )

        # remove temp file
        os.remove(meta_path_dir)
        os.remove(file_path_dir)

        return ("import success", current_version)

    else:
        # sql_helper.rollback()
        return ("import failed",)
