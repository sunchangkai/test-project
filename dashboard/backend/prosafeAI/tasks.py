# -*- coding: utf-8 -*-
# @Time    : 2023/4/21 下午6:00
# @Author  : liuliping
# @File    : tasks.py
# @description:

from application.celery import app
from sql_helper.SQLSearch import SQLSearch, connection
import pandas as pd
import os
import datetime
from sklearn.metrics import (
    precision_recall_fscore_support,
    confusion_matrix,
    balanced_accuracy_score,
    accuracy_score,
)
import itertools
import zipfile
import shutil
import numpy as np
import json

from object_detection_calculation.bounding_box import BoundingBox
from object_detection_calculation.enumerators import BBFormat, BBType, CoordinatesType
from object_detection_calculation.coco_evaluator import get_coco_summary


@app.task
def basic_metrics_classification(
    run_id, table_id, version, result_path, *args, **kwargs
):
    sql_helper = SQLSearch()

    try:
        with open(result_path, "r", encoding="utf-8") as fr:
            data = [line.strip().split(",") for line in fr.readlines()]

        table_name = sql_helper.search(
            f"SELECT table_name_mysql FROM prosafeAI_table where id={table_id};"
        )[0]["table_name_mysql"]

        metadata = pd.read_sql(
            sql=f"SELECT * FROM {table_name} WHERE data_version={version};",
            con=connection,
        )

        for sub in data:
            metadata.loc[
                os.path.basename(sub[0]) == metadata["image_name"], "predict"
            ] = sub[1]

        metadata = metadata.dropna()

        labels = list(set(metadata["class"]))

        results = calculate_classification_metrics(metadata, labels)

        # calculate slices dataset
        slice_results = {"one_odd": {}, "two_odd": {}}
        field_info = {}
        fields = sql_helper.search(
            str_sql=f"SELECT field_name FROM prosafeAI_field WHERE table_id={table_id} and field_category != '';"
        )

        for field in fields:
            field_name = field["field_name"]
            field_value = sql_helper.search(
                str_sql=f"SELECT {field_name} from {table_name} WHERE data_version={version} GROUP BY {field_name};"
            )

            # for val in field_value:
            #     field_info.setdefault(field_name, []).append(val[field_name])

            field_info[field_name] = [val[field_name] for val in field_value]

        # one odd slices
        for field, values in field_info.items():
            for value in values:
                slice_result = calculate_classification_metrics(
                    metadata[metadata[field] == value], labels
                )
                slice_results["one_odd"].setdefault(f"{field}", {}).setdefault(
                    f"{value}", slice_result
                )

            slice_results["one_odd"].setdefault(f"{field}", {}).setdefault(
                "values", values
            )

        # two odd slices
        for field1, field2 in itertools.combinations(field_info, 2):
            for value1, value2 in itertools.product(
                field_info[field1], field_info[field2]
            ):
                slice_data = metadata[
                    (metadata[field1] == value1) & (metadata[field2] == value2)
                ]

                slice_result = calculate_classification_metrics(slice_data, labels)

                slice_results["two_odd"].setdefault(
                    f"{field1}*{field2}", {}
                ).setdefault(f"{value1}*{value2}", slice_result)

            slice_results["two_odd"].setdefault(f"{field1}*{field2}", {}).setdefault(
                "values",
                {f"{field1}": field_info[field1], f"{field2}": field_info[field2]},
            )

        final_result = {
            "basic_metrics": results,
            "slices_basic_metrics": slice_results,
            "labels": labels,
            "total_samples": len(metadata),
        }

        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql_helper.update(
            str_sql=f"""UPDATE prosafeAI_modelV_run SET result_path="{result_path}", end_time="{end_time}",
                                celery_result="{final_result}", status="SUCCESS",
                                traceback="" WHERE id={run_id};"""
        )

        return final_result

    except Exception as e:
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql_helper.update(
            str_sql=f"""UPDATE prosafeAI_modelV_run SET result_path="{result_path}", end_time="{end_time}",
                                traceback="{e.__str__()}", 
                                status="FAILURE" WHERE id={run_id};"""
        )

        return e.__str__()


@app.task
def robustness_classification(run_id, table_id, version, result_path, *args, **kwargs):
    unzip_path = result_path.replace(".zip", "")

    if not zipfile.is_zipfile(result_path):
        return "zipfile is error"

    sql_helper = SQLSearch()

    try:
        # calculate dataset distribution

        report_path = sql_helper.search(
            str_sql=f"SELECT report_path from prosafeAI_modelV_check_report WHERE run_id={run_id} AND `status`='PASS';"
        )

        if not report_path:
            return "Data did not pass the check"

        with open(report_path[0]["report_path"], "r", encoding="utf-8") as fr:
            check_data = [line.strip().split(",") for line in fr.readlines()]

        table_name = sql_helper.search(
            f"SELECT table_name_mysql FROM prosafeAI_table where id={table_id};"
        )[0]["table_name_mysql"]

        metadata = pd.read_sql(
            sql=f"SELECT * FROM {table_name} WHERE data_version={version};",
            con=connection,
        )

        for sub in check_data:
            metadata.loc[os.path.basename(sub[0]) == metadata["image_name"], "flag"] = 1

        metadata = metadata[metadata["flag"] == 1]

        labels = list(set(metadata["class"]))

        # calculate robustness
        with zipfile.ZipFile(result_path) as file:
            file.extractall(unzip_path)

        for root_path, dir, files in os.walk(unzip_path):
            if dir:
                with open(
                    os.path.join(root_path, dir[0], "all_records.txt"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    all_records = f.readlines()

        data = pd.DataFrame(
            [
                {
                    sub.split(":")[0]: sub.split(":")[1]
                    for sub in line.strip().split(",")
                }
                for line in all_records
            ]
        )

        attack_methods = list(set(data["mutated_method"]))

        final_results = {
            "total_samples": len(metadata),
            "total_attack_samples": len(data),
            "labels": labels,
            "label_slices": {},
            "method_slices": {},
            "label_method_slices": {},
        }

        distribution = {}

        distance_info = {
            d: [
                data[d].astype("float").abs().min(),
                data[d].astype("float").abs().max(),
            ]
            for d in ["l0", "l1", "l2", "linf", "ssim"]
        }

        final_results["total_distance"] = calculate_classification_robustness_metrics(
            data, distance_info
        )

        for label in labels:
            distribution[label] = len(metadata[metadata["class"] == label])

            result = calculate_classification_robustness_metrics(
                data[data["label"] == label], distance_info
            )

            final_results["label_slices"].setdefault(label, {}).update(result)

        final_results["distribution"] = distribution

        for method in attack_methods:
            result = calculate_classification_robustness_metrics(
                data[data["mutated_method"] == method], distance_info
            )

            final_results["method_slices"].setdefault(method, {}).update(result)

        for label, method in itertools.product(labels, attack_methods):
            result = calculate_classification_robustness_metrics(
                data[(data["label"] == label) & (data["mutated_method"] == method)],
                distance_info,
            )

            final_results["label_method_slices"].setdefault(
                f"{label}*{method}", {}
            ).update(result)

        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql_helper.update(
            str_sql=f"""UPDATE prosafeAI_modelV_run SET result_path="{result_path}", end_time="{end_time}",
                            celery_result="{final_results}", status="SUCCESS",
                            traceback="" WHERE id={run_id};"""
        )

        return final_results

    except Exception as e:
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql_helper.update(
            str_sql=f"""UPDATE prosafeAI_modelV_run SET result_path="{result_path}", end_time="{end_time}",
                                traceback="{e.__str__()}", 
                                status="FAILURE" WHERE id={run_id};"""
        )

        return e.__str__()


@app.task
def basic_metrics_object_detection(
    run_id, table_id, version, result_path, hyperparameter, *args, **kwargs
):
    sql_helper = SQLSearch()

    try:
        with open(result_path, "r", encoding="utf-8") as fr:
            data = json.loads(fr.read())

        table_name = sql_helper.search(
            f"SELECT table_name_mysql FROM prosafeAI_table where id={table_id};"
        )[0]["table_name_mysql"]

        str_sql = (
            f"SELECT table_name_mysql from prosafeAI_table where parent_id={table_id} "
        )
        where1 = 'and table_type="object"'
        where2 = 'and table_type="tag"'

        object_table_name = sql_helper.search(str_sql + where1)[0]["table_name_mysql"]

        tag_table_name = sql_helper.search(str_sql + where2)[0]["table_name_mysql"]

        # get bounding boxes

        metadata = pd.read_sql(
            sql=f"SELECT * FROM {table_name} WHERE data_version={version};",
            con=connection,
        )

        for img, info in data.items():
            row = metadata.loc[metadata["image_name"] == os.path.basename(img)]

            if not row.empty:
                object_info = sql_helper.search(
                    str_sql=f"""
                            SELECT a.object_class, b.content from {object_table_name} a
                            JOIN {tag_table_name} b on a.id=b.object_id 
                            WHERE a.data_version={version} and a.metadata_sample_id={row["id"].values[0]} 
                            and b.feature like '%bbox%';"""
                )

                metadata.loc[row.index, "ground"] = str(
                    [
                        {
                            "bbox": eval(object["content"]),
                            "class": object["object_class"],
                        }
                        for object in object_info
                    ]
                )

                metadata.loc[row.index, "predict"] = str(info)

        metadata = metadata.dropna()  # 获取数据的子集

        label_map = sql_helper.search(
            str_sql=f"SELECT label_map from prosafeAI_version WHERE table_id={table_id} and version={version}; "
        )

        labels = (
            [label for label in eval(label_map[0]["label_map"]).values()]
            if label_map
            else []
        )

        # for label in metadata["labels"]:
        #     labels.extend(label.split(","))
        #
        # labels = list(set(labels))

        # bbox_type = hyperparamter["bbox_type"]

        results = calculate_detection_metrics(metadata, hyperparameter)

        # calculate slices dataset
        slice_results = {}

        field_info = {}
        fields = sql_helper.search(
            str_sql=f"SELECT field_name FROM prosafeAI_field WHERE table_id={table_id} and field_category != '';"
        )

        for field in fields:
            field_name = field["field_name"]
            field_value = sql_helper.search(
                str_sql=f"SELECT {field_name} from {table_name} WHERE data_version={version} GROUP BY {field_name};"
            )

            field_info[field_name] = [val[field_name] for val in field_value]

        # one odd slices
        for field, values in field_info.items():
            for value in values:
                slice_result = calculate_detection_metrics(
                    metadata[metadata[field] == value], hyperparameter
                )
                slice_results.setdefault(f"{field}", {}).setdefault(
                    f"{value}", slice_result
                )

            slice_results.setdefault(f"{field}", {}).setdefault("values", values)

        final_result = {
            "basic_metrics": results,
            "slices_basic_metrics": slice_results,
            "labels": labels,
            "total_samples": len(metadata),
        }

        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql_helper.update(
            str_sql=f"""UPDATE prosafeAI_modelV_run SET result_path="{result_path}", end_time="{end_time}",
                                                    celery_result="{final_result}", status="SUCCESS",
                                                    traceback="" WHERE id={run_id};"""
        )

        return final_result

    except Exception as e:
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql_helper.update(
            str_sql=f"""UPDATE prosafeAI_modelV_run SET result_path="{result_path}", end_time="{end_time}",
                        traceback="{e.__str__()}", 
                        status="FAILURE" WHERE id={run_id};"""
        )

        return e.__str__()


@app.task
def robustness_object_detection(
    run_id, table_id, version, result_path, *args, **kwargs
):
    unzip_path = result_path.replace(".zip", "")

    if not zipfile.is_zipfile(result_path):
        return "zipfile is error"

    sql_helper = SQLSearch()

    try:
        # calculate dataset distribution

        report_path = sql_helper.search(
            str_sql=f"SELECT report_path from prosafeAI_modelV_check_report WHERE run_id={run_id} AND `status`='PASS';"
        )

        if not report_path:
            return "Data did not pass the check"

        with open(report_path[0]["report_path"], "r", encoding="utf-8") as fr:
            check_data = [line.strip().split(",") for line in fr.readlines()]

        table_name = sql_helper.search(
            f"SELECT table_name_mysql FROM prosafeAI_table where id={table_id};"
        )[0]["table_name_mysql"]

        # str_sql = (
        #     f"SELECT table_name_mysql from prosafeAI_table where parent_id={table_id} "
        # )
        # where1 = 'and table_type="object"'
        # where2 = 'and table_type="tag"'
        #
        # object_table_name = sql_helper.search(str_sql + where1)[0]["table_name_mysql"]
        #
        # tag_table_name = sql_helper.search(str_sql + where2)[0]["table_name_mysql"]

        metadata = pd.read_sql(
            sql=f"SELECT * FROM {table_name} WHERE data_version={version};",
            con=connection,
        )

        label_map = sql_helper.search(
            str_sql=f"SELECT label_map from prosafeAI_version WHERE table_id={table_id} and version={version}; "
        )

        labels = (
            [label for label in eval(label_map[0]["label_map"]).values()]
            if label_map
            else []
        )

        for sub in check_data:
            metadata.loc[os.path.basename(sub[0]) == metadata["image_name"], "flag"] = 1

        metadata = metadata[metadata["flag"] == 1]

        # for sub in metadata:
        #
        #     object_info = sql_helper.search(
        #         str_sql=f"""
        #                 SELECT a.object_class, b.content from {object_table_name} a
        #                 JOIN {tag_table_name} b on a.id=b.object_id
        #                 WHERE a.data_version={version} and a.metadata_sample_id={sub["id"].values[0]}
        #                 and b.feature like '%bbox%';"""
        #     )
        #
        #     metadata.loc[sub.index, "ground"] = str(
        #         [
        #             {
        #                 "bbox": eval(object["content"]),
        #                 "class": object["object_class"],
        #             }
        #             for object in object_info
        #         ]
        #     )

        # labels = list(set(metadata["class"]))

        # calculate robustness
        with zipfile.ZipFile(result_path) as file:
            file.extractall(unzip_path)

        for root_path, dir, files in os.walk(unzip_path):
            if dir:
                with open(
                    os.path.join(root_path, dir[0], "all_records.txt"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    all_records = f.readlines()

        data = pd.DataFrame(
            [
                {
                    sub.split(":")[0]: sub.split(":")[1]
                    for sub in line.strip().split(",")
                }
                for line in all_records
            ]
        )

        attack_methods = list(set(data["mutated_method"]))

        final_results = {
            "total_samples": len(metadata),
            "total_attack_samples": len(data),
            "labels": labels,
            # "label_slices": {},
            "method_slices": {},
            # "label_method_slices": {},
        }

        # distribution = {}

        distance_info = {
            d: [
                data[d].astype("float").abs().min(),
                data[d].astype("float").abs().max(),
            ]
            for d in ["l0", "l1", "l2", "linf", "ssim"]
        }

        final_results["total_distance"] = calculate_detection_robustness_metrics(
            data, distance_info
        )

        # for label in labels:
        #
        #     distribution[label] = len(metadata[metadata["class"] == label])
        #
        #     result = calculate_detection_robustness_metrics(
        #         data[data["label"] == label], distance_info
        #     )
        #
        #     final_results["label_slices"].setdefault(label, {}).update(result)
        #
        # final_results["distribution"] = distribution

        for method in attack_methods:
            result = calculate_detection_robustness_metrics(
                data[data["mutated_method"] == method], distance_info
            )

            final_results["method_slices"].setdefault(method, {}).update(result)

        # for label, method in itertools.product(labels, attack_methods):
        #     result = calculate_detection_robustness_metrics(
        #         data[(data["label"] == label) & (data["mutation_method"] == method)],
        #         distance_info,
        #     )
        #
        #     final_results["label_method_slices"].setdefault(
        #         f"{label}*{method}", {}
        #     ).update(result)

        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql_helper.update(
            str_sql=f"""UPDATE prosafeAI_modelV_run SET result_path="{result_path}", end_time="{end_time}",
                            celery_result="{final_results}", status="SUCCESS",
                            traceback="" WHERE id={run_id};"""
        )

        return final_results

    except Exception as e:
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql_helper.update(
            str_sql=f"""UPDATE prosafeAI_modelV_run SET result_path="{result_path}", end_time="{end_time}",
                                traceback="{e.__str__()}", 
                                status="FAILURE" WHERE id={run_id};"""
        )

        return e.__str__()


def calculate_classification_metrics(data: pd.DataFrame, labels=None):
    if len(data):
        micro_result = precision_recall_fscore_support(
            data["class"],
            data["predict"],
            average="micro",
            labels=labels,
            zero_division=0,
        )
        macro_result = precision_recall_fscore_support(
            data["class"],
            data["predict"],
            average="macro",
            labels=labels,
            zero_division=0,
        )
        weighted_result = precision_recall_fscore_support(
            data["class"],
            data["predict"],
            average="weighted",
            labels=labels,
            zero_division=0,
        )

        balance_accuracy = balanced_accuracy_score(data["class"], data["predict"])
        accuracy = accuracy_score(data["class"], data["predict"])
        matrix = confusion_matrix(data["class"], data["predict"], labels=labels)

        results = {
            "distribution": {
                label: len(data[data["class"] == label]) for label in labels
            },
            "samples": len(data),
            "matrix": matrix.tolist(),
            "balance*accuracy": round(balance_accuracy, 3),
            "total*accuracy": round(accuracy, 3),
        }

        for key, res in {
            "micro": micro_result,
            "macro": macro_result,
            "weighted": weighted_result,
        }.items():
            results[f"{key}*precision"] = round(res[0], 3)
            results[f"{key}*recall"] = round(res[1], 3)
            results[f"{key}*f1score"] = round(res[2], 3)

    else:
        results = {
            "distribution": {},
            "samples": 0,
            "matrix": [[]],
            "balance*accuracy": 0,
            "total*accuracy": 0,
        }
        for key in {"micro", "macro", "weighted"}:
            results[f"{key}*precision"] = 0
            results[f"{key}*recall"] = 0
            results[f"{key}*f1score"] = 0

    return results


def calculate_detection_metrics(data: pd.DataFrame, hyperparameter):
    if len(data):
        hyperparameter = eval(hyperparameter)

        ground_bbox, predict_bbox = [], []
        for idx, sub in data.iterrows():
            for label in eval(sub["ground"]):
                ground_bbox.append(
                    BoundingBox(
                        image_name=sub["image_name"],
                        class_id=label["class"],
                        coordinates=label["bbox"],
                        type_coordinates=CoordinatesType.RELATIVE
                        if hyperparameter["scale"]
                        else CoordinatesType.ABSOLUTE,
                        img_size=list(eval(sub["image_size"]).values()),
                        confidence=1,
                        bb_type=BBType.GROUND_TRUTH,
                        format=BBFormat[hyperparameter["bbox_type"]],
                    )
                )

            for pred in eval(sub["predict"]):
                # default cxcyw(YOLO)

                predict_bbox.append(
                    BoundingBox(
                        image_name=sub["image_name"],
                        class_id=pred["class"],
                        coordinates=pred["bbox"],
                        type_coordinates=CoordinatesType.ABSOLUTE,
                        img_size=list(eval(sub["image_size"]).values()),
                        confidence=pred["confidence"],
                        bb_type=BBType.DETECTED,
                        format=BBFormat.XYX2Y2,
                    )
                )

        results = get_coco_summary(ground_bbox, predict_bbox)

    else:
        iou_thresholds = np.linspace(
            0.5, 0.95, int(np.round((0.95 - 0.5) / 0.05)) + 1, endpoint=True
        )

        results = {
            round(iou, 2): {
                "detail": [],
                "mAP": 0.0,
                "micro*precision": 0.0,
                "micro*recall": 0.0,
                "micro*f1score": 0.0,
                "macro*precision": 0.0,
                "macro*recall": 0.0,
                "macro*f1score": 0.0,
                "weighted*precision": 0.0,
                "weighted*recall": 0.0,
                "weighted*f1score": 0.0,
            }
            for iou in iou_thresholds
        }

    return results


def calculate_classification_robustness_metrics(
    data: pd.DataFrame, distance_info, num=10
):
    attack_samples = len(data)

    attack_success = len(data[data["label"] != data["pred_label"]])

    distance_detail = {}

    for distance, values in distance_info.items():
        format_data = data[distance].astype("float").abs()

        distance_min, distance_max = values

        stride = (distance_max - distance_min) / num

        for i in range(num):
            sub_data = data[
                (format_data >= stride * i) & (format_data < stride * (i + 1))
            ]

            sub_attack_sample = len(sub_data)

            sub_attack_success = len(
                sub_data[sub_data["label"] != sub_data["pred_label"]]
            )

            ASR = (
                round(sub_attack_success / sub_attack_sample, 3)
                if sub_attack_success
                else 0
            )

            distance_detail.setdefault(distance, {}).setdefault(
                round((stride * i) + stride / 2, 3), ASR
            )

    return {
        "attack_samples": attack_samples,
        "attack_success": attack_success,
        "attack_failed": attack_samples - attack_success,
        "ASR": round(attack_success / attack_samples, 3) if attack_success else 0,
        "distance_detail": distance_detail,
    }


def calculate_detection_robustness_metrics(data: pd.DataFrame, distance_info, num=10):
    attack_samples = len(data)

    attack_success = len(data[data["attack_status"] == "success"])

    distance_detail = {}

    for distance, values in distance_info.items():
        format_data = data[distance].astype("float").abs()

        distance_min, distance_max = values

        stride = (distance_max - distance_min) / num

        for i in range(num):
            sub_data = data[
                (format_data >= stride * i) & (format_data < stride * (i + 1))
            ]

            sub_attack_sample = len(sub_data)

            sub_attack_success = len(sub_data[sub_data["attack_status"] == "success"])

            ASR = (
                round(sub_attack_success / sub_attack_sample, 3)
                if sub_attack_success
                else 0
            )

            distance_detail.setdefault(distance, {}).setdefault(
                round((stride * i) + stride / 2, 3), ASR
            )

    return {
        "attack_samples": attack_samples,
        "attack_success": attack_success,
        "attack_failed": attack_samples - attack_success,
        "ASR": round(attack_success / attack_samples, 3) if attack_success else 0,
        "distance_detail": distance_detail,
    }


if __name__ == "__main__":
    # print(basic_metrics_classification(12, 1, 1, result_path='/backend/metadata_1_version_1.txt'))
    # print(
    #     robustness_classification(
    #         128,
    #         1,
    #         1,
    #         result_path="/backend/sdk_results/results-2023-06-14_13:50:56.zip",
    #     )
    # )
    print(
        basic_metrics_object_detection(
            208,
            13,
            2,
            result_path="../sdk_results/bdd100k_predict_results.json",
            hyperparameter='{"bbox_type": "XYX2Y2", "scale": 0}',
        )
    )
    # print(
    #     robustness_object_detection(
    #         203,
    #         10,
    #         2,
    #         result_path="/data/sdk_results/2023/9/results-2023-09-20_15:40:40.zip",
    #     )
    # )
