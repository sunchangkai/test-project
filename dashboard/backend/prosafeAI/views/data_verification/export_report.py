# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 上午10:33
# @Author  : xiaxi
# @File    : export_report.py
# @description:

# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import mm, inch, cm
# from reportlab.lib.colors import Color
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib import colors
# from reportlab.platypus import (
#     Flowable,
#     SimpleDocTemplate,
#     Image,
#     Paragraph,
#     PageBreak,
#     TableStyle,
#     Table,
#     Spacer,
# )
# from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
# from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
# from reportlab.lib.utils import ImageReader
#
#
# from pdfrw import PdfReader
# from pdfrw.buildxobj import pagexobj
# from pdfrw.toreportlab import makerl

from prosafeAI.views.data_verification.dataV_report import data_verification_report
from sql_helper.SQLSearch import SQLSearch
from django.http import FileResponse, Http404, HttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework.views import APIView

import os

# import matplotlib
# import datetime
# from datetime import datetime
# matplotlib.use("PDF")
# import matplotlib.pyplot as plt
# import io
# import numpy as np
# from numpy import arange
# from textwrap import fill
# from itertools import combinations
from dvadmin.utils.json_response import ErrorResponse


class ExportReportView(APIView):
    def get(self, request):
        task_id = request.query_params.get("task_id")
        filename = "report.pdf"

        if not task_id:
            return ErrorResponse(msg="task_id is required")

        try:
            data_userinfo = get_task_info(task_id)
            data_result = get_result_info(task_id)

            # 生成report.pdf
            data_verification_report(filename, task_id, data_userinfo, data_result)

            # pdfmetrics.registerFont(
            #     TTFont(
            #         "Arial",
            #         os.path.join(os.getcwd(), "static/rest_framework/fonts/Arial.ttf"),
            #     )
            # )
            # styles = getSampleStyleSheet()
            # styles["Normal"].spaceBefore = 10
            # styles["Normal"].spaceAfter = 10
            #
            # elements = [Paragraph("Data Verification Report", style_dict["title"])]
            # if data_userinfo:
            #     elements.append(drawUserInfoTable(userinfo_data=data_userinfo))
            #     elements.append(Spacer(1, 3 * mm))
            #
            #     elements.append(
            #         Paragraph(
            #             "Results of data verification are shown as below:",
            #             styles["Normal"],
            #         )
            #     )
            #     elements.append(Spacer(1, 2 * mm))
            #
            #     if data_result:
            #         elements.append(ResultTable(data_summary=data_result))
            #     else:
            #         elements.append(
            #             Paragraph(
            #                 "The verification results can be obtained only after the data validation task is established",
            #                 styles["Normal"],
            #             )
            #         )
            #
            #     elements.append(Spacer(1, 3 * mm))
            #     elements.append(PageBreak())
            #
            #     elements.append(Paragraph("Appendix", style=styles["Heading1"]))
            #     ptext = "1.  Dataset Summary"
            #     elements.append(Paragraph(ptext, style=styles["Heading2"]))
            #     ptext = "1.1  # samples & labels distribution"
            #     elements.append(Paragraph(ptext, style=styles["Heading3"]))
            #
            #     dataset_info, label_data = get_dataset_info(task_id)
            #
            #     samples_number = dataset_info["count"]
            #     dataset_description = dataset_info["table_description"]
            #     version_number = dataset_info["version"]
            #
            #     ptext = f"""There are <strong>{samples_number}</strong> samples in datasets <strong>{dataset_description}</strong> with version <strong>{version_number}</strong> in all."""
            #     elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #     if label_data:
            #         ptext = f"""The distribution of label categories on the dataset is shown as below:"""
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #         elements.append(Spacer(1, 0.2 * inch))
            #         elements.append(
            #             label_distributions(data=label_data, colors_list=colors_list)
            #         )
            #     else:
            #         ptext = f"""Only one field is allowed to be a label,
            #         so the distribution of label categories on the dataset cannot be displayed."""
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #     elements.append(Spacer(1, 0.2 * inch))
            #     ptext = "1.2  Feature name list"
            #     elements.append(Paragraph(ptext, style=styles["Heading3"]))
            #     feature_name_list, feature_data = get_feature_names(
            #         table_name=dataset_info["table_name"],
            #         version=dataset_info["version"],
            #         table_id=dataset_info["table_id"],
            #     )
            #     if feature_name_list:
            #         features_for_heatmap = list(feature_data.keys())
            #         ptext = f"""From the metadata of the dataset, there are <strong>{len(features_for_heatmap)}</strong> features
            #         whose number of distinct values within the range of[2,10].
            #         """
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #         ptext = f"""The feature names and their values are shown in the following table:
            #         """
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #         elements.append(feature_table(data=feature_name_list))
            #     else:
            #         ptext = f"""From the metadata of the dataset, we can't find the features
            #         whose number of distinct value within range [2,10])"""
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #     ptext = "1.3  Feature distribution display"
            #     elements.append(Paragraph(ptext, style=styles["Heading3"]))
            #
            #     if feature_data:
            #         ptext = f"""
            #         The distribution chart of each feature on the number of samples is displayed as follows.
            #         """
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #         elements.append(Spacer(1, 0.2 * inch))
            #         elements = draw_features_images(elements, feature_data)
            #     else:
            #         ptext = f"""As there is no feature whose number of distinct values within the range [2,10]),
            #         the distribution chart cannot be displayed."""
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #     ptext = "1.4   Double ODD cross coverage heatmap display"
            #     elements.append(Paragraph(ptext, style=styles["Heading3"]))
            #
            #     if (not feature_data) or (len(list(feature_data.keys())) < 2):
            #         ptext = "As the number of available feature is less than two, the heatmap of odd cross coverage cannot be displayed."
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #     else:
            #         features_for_heatmap = list(feature_data.keys())
            #         feature_text = ", ".join(
            #             [item for item in features_for_heatmap if item is not None]
            #         )
            #
            #         ptext = f"""
            #         In this section, ODD cross coverage statistics are conducted between the <strong>{len(features_for_heatmap)}</strong> features in pairs.
            #         """
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #
            #         ptext = f"""
            #         For the features <strong>{feature_text}</strong>, the following <strong>{len(list(combinations(features_for_heatmap, 2)))}</strong> heat maps are generated accordingly:
            #         """
            #
            #         elements.append(Paragraph(ptext, style=styles["Normal"]))
            #         elements.append(Spacer(1, 0.1 * inch))
            #
            #         elements = draw_heatmap_two_in_row(
            #             table_name=dataset_info["table_name"],
            #             version=dataset_info["version"],
            #             feature_data=feature_data,
            #             elements=elements,
            #         )
            #
            #     ptext = (
            #         "2.  Data coverage details within scenarios from data requirements"
            #     )
            #     elements.append(Paragraph(ptext, style=styles["Heading2"]))
            #     ptext = "2.1.  ODD parameters list"
            #     elements.append(Paragraph(ptext, style=styles["Heading3"]))
            #
            #     ptext = "2.2.  ODD data coverage display"
            #     elements.append(Paragraph(ptext, style=styles["Heading3"]))
            # else:
            #     elements.append(
            #         Paragraph(
            #             "Can not find any information for this data verification task.",
            #             styles["Normal"],
            #         )
            #     )
            #
            # doc = SimpleDocTemplate(
            #     filename,
            #     pagesize=A4,
            #     topMargin=2 * cm,
            #     bottomMargin=2 * cm,
            #     leftMargin=1 * cm,
            #     rightMargin=1 * cm,
            # )
            # doc.build(elements, canvasmaker=PageNumCanvas)

            path = os.path.join(os.getcwd(), filename)
            response = HttpResponse(content_type="application/pdf;charset=utf-8")
            response["Access-Control-Expose-Headers"] = "Content-Disposition"
            response["Content-Disposition"] = "attachment;filename*=UTF-8''{}".format(
                escape_uri_path(filename)
            )

            with open(path, "rb") as f:
                response.write(f.read())

            return response

        except Exception as e:
            return ErrorResponse(msg=e.__str__())


# global variables, e.g. color list, styles of title or tables
# colors_list = [
#     "springgreen",
#     "cyan",
#     "deepskyblue",
#     "royalblue",
#     "navy",
#     "darkorchid",
#     "magenta",
#     "violet",
#     "lightpink",
#     "orangered",
#     "salmon",
#     "orange",
#     "gold",
# ]
#
# style_dict = {
#     "title": ParagraphStyle(
#         name="Title",
#         fontName="Arial",
#         fontSize=22,
#         leading=16,
#         alignment=1,
#         spaceAfter=20,
#     ),
#     # Define table style
#     "tblstyle": TableStyle(
#         [
#             ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.white),
#             ("BOX", (0, 0), (-1, -1), 0.25, colors.white),
#             ("FONTSIZE", (0, 0), (-1, 0), 7),
#             ("FONTSIZE", (0, 1), (-1, -1), 7),
#             ("TEXTFONT", (0, 0), (-1, 0), "Calibri-Bold"),
#             ("TEXTFONT", (0, 1), (0, -1), "Calibri-Bold"),
#             ("TEXTFONT", (0, 1), (-1, -1), "Calibri"),
#             ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#             # ('TEXTCOLOR', (1, 1), (0, -1), colors.black),
#             ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
#             ("LEFTPADDING", (0, 0), (-1, -1), 1),
#             ("RIGHTPADDING", (0, 0), (-1, -1), 1),
#             ("TOPPADDING", (0, 0), (-1, -1), 6),
#             ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
#             (
#                 "ROWBACKGROUNDS",
#                 (0, 0),
#                 (-1, -1),
#                 (colors.HexColor("#e8e9ec"), colors.HexColor("#CED1D6")),
#             ),
#             ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3A5675")),
#             ("ALIGN", (0, 0), (-1, 0), "CENTER"),
#             ("ALIGN", (0, 1), (-1, -1), "CENTER"),
#             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#         ]
#     ),
#     "userinfo_style": TableStyle(
#         [
#             ("FONT", (0, 0), (-1, -1), "Arial", 8),
#             ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
#             ("ALIGN", (1, 0), (1, -1), "CENTER"),
#         ]
#     ),
# }
#
#
# get data from sql
def get_task_info(task_id):
    sql_helper = SQLSearch()

    str_sql = f"""
            SELECT F.name as project_name, F.project_manager, E.name as usercase_name, B.`task_name`, C.`table_description`, 
            B.`version`, A.`name` AS requirements, B.`test_begin_time`, B.`test_end_time`, B.`status`, B.`requirements_id`, 
            DATE_FORMAT(A.`create_time`, '%m/%d/%Y %H:%i:%s') as requirement_create_time
            FROM prosafeAI_data_verification_task B
            INNER JOIN prosafeAI_data_requirements A ON A.id=B.requirements_id
            INNER JOIN prosafeAI_table C ON C.id=B.table_id
            INNER JOIN prosafeAI_usercase E ON E.id=C.usercase_id
            INNER JOIN prosafeAI_project F ON F.id=E.project_id
        WHERE C.table_type='metadata' and B.id={task_id}
    """

    data = sql_helper.search(str_sql)

    if data:
        data_info = [
            ["Project Name", data[0]["project_name"]],
            ["Project Owner", data[0]["project_manager"]],
            ["Usercase Name", data[0]["usercase_name"]],
            ["Datasets", data[0]["table_description"]],
            ["Data Version", data[0]["version"]],
            ["Test Time", data[0]["test_begin_time"]],
            ["Data Requirements", data[0]["requirements"]],
        ]
    else:
        data_info = []
    return data_info
#
#
def get_result_info(task_id):
    sql_helper = SQLSearch()

    str_sql_result = f"""
    SELECT A.`rule_name`, A.`classification`, A.`verification_object`, A.`verification_content`, B.`test_result`, B.`result_description`
    FROM prosafeAI_data_sub_requirements A
        LEFT JOIN prosafeAI_data_verification_result B ON A.requirements_id=B.requirements_id and A.id=B.sub_requirements_id
    WHERE B.task_id={task_id}
    """
    data = sql_helper.search(str_sql_result)
    if data:
        keys = list(data[0].keys())
        data_result = [keys]
        for item in range(len(data)):
            item_result = [data[item][keys[key_item]] for key_item in range(len(keys))]
            data_result.append(item_result)
    else:
        data_result = False
    return data_result
#
#
# def get_dataset_info(task_id):
#     sql_helper = SQLSearch()
#     str_sql = f"""
#     SELECT B.`table_name_mysql`, B.`table_description`, A.`version`, A.`table_id`
#     FROM prosafeAI_data_verification_task A
#     INNER JOIN prosafeAI_table B ON B.id=A.table_id
#     WHERE B.table_type='metadata' and A.id={task_id}
#     """
#     data = sql_helper.search(str_sql)
#     table_name = data[0]["table_name_mysql"]
#     version = data[0]["version"]
#     table_id = data[0]["table_id"]
#
#     str_sql2 = f"""
#     SELECT count(*) as count from {table_name} where  data_version={version}
#     """
#     data2 = sql_helper.search(str_sql2)
#     dataset_info = {
#         "table_description": data[0]["table_description"],
#         "table_name": table_name,
#         "version": version,
#         "count": data2[0]["count"],
#         "table_id": table_id,
#     }
#
#     str_sql3_1 = f"""
#     SELECT count(field_name) as count FROM prosafeAI_field where table_id = {table_id} and field_category = 'label'
#     """
#     label_count = sql_helper.search(str_sql3_1)[0]["count"]
#
#     if label_count == 1:
#         str_sql3 = f"""
#         SELECT field_name FROM prosafeAI_field where table_id = {table_id} and field_category = 'label'
#         """
#         label_name = sql_helper.search(str_sql3)[0]["field_name"]
#
#         str_sql4 = f"""
#         SELECT {label_name}, count(id) as VALUE FROM {table_name} WHERE data_version={version} GROUP BY {label_name}
#         """
#
#         label_name_list = sql_helper.search(str_sql4)
#
#         label_data = {}
#         class_list = []
#         value_list = []
#         for item in range(len(label_name_list)):
#             class_list.append(label_name_list[item][label_name])
#             value_list.append(label_name_list[item]["VALUE"])
#
#         label_data["categories"] = class_list
#         label_data["values"] = value_list
#
#     else:
#         label_data = False
#
#     return dataset_info, label_data
#
#
# def get_feature_names(table_name, version, table_id):
#     sql_helper = SQLSearch()
#     str_sql = f"""
#     SELECT field_name from prosafeAI_field where table_id ={table_id}
#     """
#     names_tmp = sql_helper.search(str_sql)
#
#     names = [names_tmp[item]["field_name"] for item in range(len(names_tmp))]
#
#     str_begin = "select "
#     for name_item in range(len(names)):
#         str_slice = f"""count(distinct({names[name_item]})) as {names[name_item]},"""
#         str_begin += str_slice
#     new_str = str_begin.rstrip(",")
#     last_str = f"""
#      from {table_name} where data_version={version}
#     """
#     str_sql2 = new_str + last_str
#     counts = sql_helper.search(str_sql2)[0]
#
#     name_value_dict = dict(filter(lambda x: x[1] > 1 and x[1] < 10, counts.items()))
#
#     if name_value_dict:
#         name_list = list(name_value_dict.keys())
#         value_list = list(name_value_dict.values())
#
#         new_name_str = ", ".join(name_list)
#
#         str_sql_temp = "select " + name_list[0] + " from a "
#         for item_name in range(len(name_list)):
#             temp_slice = f"""
#             UNION select {name_list[item_name]} from a
#             """
#             str_sql_temp += temp_slice
#
#         str_sql3 = f"""
#         WITH a AS
#         (SELECT {new_name_str} from {table_name} where data_version={version})
#         {str_sql_temp}
#         """
#         feature_names = sql_helper.search(str_sql3)
#
#         feature_values = [
#             feature_names[item][name_list[0]] for item in range(len(feature_names))
#         ]
#         flag = 0
#         feature_name_list = [["Feature Name", "Feature Values", "No. of Values"]]
#         for item in range(len(value_list)):
#             a = str(feature_values[flag : flag + value_list[item]])
#             flag += value_list[item]
#             feature_name_list.append([name_list[item], a, value_list[item]])
#
#         feature_data = {}
#         for item in range(len(name_list)):
#             str_sql4 = f"""
#             select {name_list[item]}, count(id) as value from {table_name} where data_version={version} group by {name_list[item]}
#             """
#             data = sql_helper.search(str_sql4)
#
#             data2 = {}
#             for x in range(len(data)):
#                 data2[data[x][name_list[item]]] = data[x]["value"]
#
#             feature_data[name_list[item]] = data2
#
#     else:
#         feature_name_list = False
#         feature_data = False
#
#     return feature_name_list, feature_data
#
#
# # draw odd coverage heatmap with two figures in one row
# def draw_heatmap_two_in_row(table_name, version, feature_data, elements):
#     items = list(feature_data.keys())
#
#     com_list = list(combinations(items, 2))
#     coms_len = len(com_list)
#
#     for item in range(round(coms_len / 2)):
#         com_1 = com_list[item * 2]  # ["a",'b']
#         data1 = prepare_heatmap_data(
#             table_name=table_name, version=version, feature_data=feature_data, com=com_1
#         )
#
#         if coms_len % 2 != 0 and item == round(coms_len / 2) - 1:
#             elements.append(two_heatmap(data_1=data1, data_2=False))
#
#         else:
#             com_2 = com_list[item * 2 + 1]
#             data2 = prepare_heatmap_data(
#                 table_name=table_name,
#                 version=version,
#                 feature_data=feature_data,
#                 com=com_2,
#             )
#
#             elements.append(two_heatmap(data_1=data1, data_2=data2))
#
#     return elements
#
#
# def two_heatmap(data_1, data_2):
#     pi = heatmap_for_features(data=data_1)
#     if data_2:
#         pi2 = heatmap_for_features(data=data_2)
#         return Table([[pi, pi2]], colWidths=[250, 250])
#     else:
#         return Table(
#             [
#                 [
#                     pi,
#                 ]
#             ]
#         )
#
#
# def prepare_heatmap_data(table_name, version, feature_data, com):
#     sql_helper = SQLSearch()
#     feature_value_1 = list(feature_data[com[0]].keys())  # ['no snow', 'light snow']
#     feature_value_2 = list(
#         feature_data[com[1]].keys()
#     )  # ['cloudy', 'sunny', 'partly sunny']
#
#     str_sql_com = f"""
#     SELECT {com[0]}, {com[1]}, count(id) as count FROM {table_name} WHERE data_version={version} GROUP BY {com[0]}, {com[1]}
#     """
#     feature_values_sql = sql_helper.search(str_sql_com)
#     data_array = np.zeros([len(feature_value_1), len(feature_value_2)], dtype=np.int32)
#
#     for item_value in range(len(feature_values_sql)):
#         x = feature_value_1.index(feature_values_sql[item_value][com[0]])
#         y = feature_value_2.index(feature_values_sql[item_value][com[1]])
#         data_array[x][y] = feature_values_sql[item_value]["count"]
#
#     if len(feature_value_1) > len(feature_value_2):
#         data = {
#             "data": data_array.T,
#             "feature_value_1": feature_value_2,
#             "feature_value_2": feature_value_1,
#             "combination": [com[1], com[0]],
#         }
#
#     else:
#         data = {
#             "data": data_array,
#             "feature_value_1": feature_value_1,
#             "feature_value_2": feature_value_2,
#             "combination": com,
#         }
#     return data
#
#
# # heatmap utils
# def heatmap(
#     data,
#     features,
#     row_labels,
#     col_labels,
#     ax=None,
#     cbar_kw=None,
#     cbarlabel="",
#     **kwargs,
# ):
#     """
#     Create a heatmap from a numpy array and two lists of labels.
#
#     Parameters
#     ----------
#     data
#         A 2D numpy array of shape (M, N).
#     row_labels
#         A list or array of length M with the labels for the rows.
#     col_labels
#         A list or array of length N with the labels for the columns.
#     ax
#         A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
#         not provided, use current axes or create a new one.  Optional.
#     cbar_kw
#         A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
#     cbarlabel
#         The label for the colorbar.  Optional.
#     **kwargs
#         All other arguments are forwarded to `imshow`.
#     """
#
#     if ax is None:
#         ax = plt.gca()
#
#     if cbar_kw is None:
#         cbar_kw = {}
#
#     # Plot the heatmap
#     im = ax.imshow(data, **kwargs)
#
#     # Create colorbar
#     cbar = ax.figure.colorbar(im, ax=ax, fraction=0.023, **cbar_kw)
#     cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
#
#     # plt.xticks(arange(len(X)), [fill(item, 13) for item in X], wrap=True, fontsize=6, labels=col_labels)
#
#     # Show all ticks and label them with the respective list entries.
#     ax.set_xticks(
#         np.arange(data.shape[1]), [fill(item, 10) for item in col_labels], wrap=True
#     )
#     ax.set_yticks(
#         np.arange(data.shape[0]), [fill(item, 10) for item in row_labels], wrap=True
#     )
#
#     ax.set_xticklabels(col_labels)
#     ax.set_yticklabels(row_labels)
#
#     # Let the horizontal axes labeling appear on top.
#     ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
#
#     # Rotate the tick labels and set their alignment.
#     plt.setp(ax.get_xticklabels(), rotation=0, ha="center", rotation_mode="anchor")
#     plt.setp(ax.get_yticklabels(), rotation=0, ha="right", rotation_mode="anchor")
#
#     # Turn spines off and create white grid.
#     ax.spines[:].set_visible(False)
#
#     ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor=True)
#     ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor=True)
#     ax.set_xlabel(f""" {features[1]} """)
#     ax.set_ylabel(f""" {features[0]} """)
#     ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
#     ax.tick_params(which="minor", bottom=False, left=False)
#     # raw_ratio = 1.5
#     # aspect_ratio = forceAspect(ax, aspect=raw_ratio)
#
#     return im, cbar
#
#
# def annotate_heatmap(
#     im,
#     data=None,
#     valfmt="{x:.2f}",
#     textcolors=("black", "white"),
#     threshold=None,
#     **textkw,
# ):
#     """
#     A function to annotate a heatmap.
#
#     Parameters
#     ----------
#     im
#         The AxesImage to be labeled.
#     data
#         Data used to annotate.  If None, the image's data is used.  Optional.
#     valfmt
#         The format of the annotations inside the heatmap.  This should either
#         use the string format method, e.g. "$ {x:.2f}", or be a
#         `matplotlib.ticker.Formatter`.  Optional.
#     textcolors
#         A pair of colors.  The first is used for values below a threshold,
#         the second for those above.  Optional.
#     threshold
#         Value in data units according to which the colors from textcolors are
#         applied.  If None (the default) uses the middle of the colormap as
#         separation.  Optional.
#     **kwargs
#         All other arguments are forwarded to each call to `text` used to create
#         the text labels.
#     """
#
#     if not isinstance(data, (list, np.ndarray)):
#         data = im.get_array()
#
#     # Normalize the threshold to the images color range.
#     if threshold is not None:
#         threshold = im.norm(threshold)
#     else:
#         threshold = im.norm(data.max()) / 2.0
#
#     # Set default alignment to center, but allow it to be
#     # overwritten by textkw.
#     kw = dict(horizontalalignment="center", verticalalignment="center")
#     kw.update(textkw)
#
#     # Get the formatter in case a string is supplied
#     if isinstance(valfmt, str):
#         valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)
#
#     # Loop over the data and create a `Text` for each "pixel".
#     # Change the text's color depending on the data.
#     texts = []
#     for i in range(data.shape[0]):
#         for j in range(data.shape[1]):
#             kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
#             text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
#             texts.append(text)
#
#     return texts
#
#
# def forceAspect(ax, aspect=1):
#     im = ax.get_images()
#     extent = im[0].get_extent()
#     ax.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)
#
#
# def heatmap_for_features(data):
#     data_info = data["data"]
#     feature_value_1 = data["feature_value_1"]
#     feature_value_2 = data["feature_value_2"]
#     features = data["combination"]
#
#     fig, ax = plt.subplots()
#     im, cbar = heatmap(
#         data_info,
#         features,
#         feature_value_1,
#         feature_value_2,
#         ax=ax,
#         cmap="YlGn",
#         cbarlabel="# of samples",
#     )
#     # texts = annotate_heatmap(im)
#     fig.tight_layout()
#     ax.set_title(f"""ODD coverage of {features[0]} and {features[1]}""")
#
#     imgdata = io.BytesIO()
#     fig.savefig(imgdata, format="png", dpi=200)
#     imgdata.seek(0)
#     image = ImageReader(imgdata)
#     img = PdfImage2(image)
#     return img
#
#
# # class for draw heatmap in pdf
# class PdfImage2(Flowable):
#     def __init__(self, img_data, width=250, height=250):
#         self.img_width = width
#         self.img_height = height
#         self.img_data = img_data
#
#     def wrap(self, width, height):
#         return self.img_width, self.img_height
#
#     def drawOn(self, canv, x, y, _sW=0):
#         if _sW > 0 and hasattr(self, "hAlign"):
#             a = self.hAlign
#             if a in ("CENTER", "CENTRE", TA_CENTER):
#                 x += 0.5 * _sW
#             elif a in ("RIGHT", TA_RIGHT):
#                 x += _sW
#             elif a not in ("LEFT", TA_LEFT):
#                 raise ValueError("Bad hAlign value " + str(a))
#         canv.saveState()
#         canv.drawImage(self.img_data, x, y, self.img_width, self.img_height)
#         canv.restoreState()
#
#
# # utils for images:
# class PdfImage(Flowable):
#     """PdfImage wraps the page from a PDF file as a Flowable
#     which can be included into a ReportLab Platypus document.
#     Based on the vectorpdf extension in rst2pdf (http://code.google.com/p/rst2pdf/)"""
#
#     def __init__(self, filename_or_object, width=None, height=None, kind="direct"):
#         # If using StringIO buffer, set pointer to beginning
#         if hasattr(filename_or_object, "read"):
#             filename_or_object.seek(0)
#         page = PdfReader(filename_or_object, decompress=False).pages[0]
#         self.xobj = pagexobj(page)
#         self.imageWidth = width
#         self.imageHeight = height
#         x1, y1, x2, y2 = self.xobj.BBox
#
#         self._w, self._h = x2 - x1, y2 - y1
#         if not self.imageWidth:
#             self.imageWidth = self._w
#         if not self.imageHeight:
#             self.imageHeight = self._h
#         self.__ratio = float(self.imageWidth) / self.imageHeight
#         if kind in ["direct", "absolute"] or width is None or height is None:
#             self.drawWidth = width or self.imageWidth
#             self.drawHeight = height or self.imageHeight
#         elif kind in ["bound", "proportional"]:
#             factor = min(float(width) / self._w, float(height) / self._h)
#             self.drawWidth = self._w * factor
#             self.drawHeight = self._h * factor
#
#     def wrap(self, aW, aH):
#         return self.drawWidth, self.drawHeight
#
#     def drawOn(self, canv, x, y, _sW=0):
#         if _sW > 0 and hasattr(self, "hAlign"):
#             a = self.hAlign
#             if a in ("CENTER", "CENTRE", TA_CENTER):
#                 x += 0.5 * _sW
#             elif a in ("RIGHT", TA_RIGHT):
#                 x += _sW
#             elif a not in ("LEFT", TA_LEFT):
#                 raise ValueError("Bad hAlign value " + str(a))
#
#         xobj = self.xobj
#         xobj_name = makerl(canv._doc, xobj)
#
#         xscale = self.drawWidth / self._w
#         yscale = self.drawHeight / self._h
#
#         x -= xobj.BBox[0] * xscale
#         y -= xobj.BBox[1] * yscale
#
#         canv.saveState()
#         canv.translate(x, y)
#         canv.scale(xscale, yscale)
#         canv.doForm(xobj_name)
#         canv.restoreState()
#
#
# def bar_distribution(data, figsize, colors_list, x_name):
#     X = data["categories"]
#     Y = data["values"]
#     my_colors = colors_list[0 : len(X)]
#
#     fig, ax = plt.subplots(figsize=figsize)
#
#     p = ax.bar(X, Y, color=my_colors)
#     ax.set_ylabel("# of samples", fontsize=8)
#     ax.set_title("The Distribution of " + x_name, fontsize=9)
#     ax.bar_label(p, fontsize=7)
#     plt.xlabel("Categories of " + x_name, fontsize=8)
#
#     plt.xticks(arange(len(X)), [fill(item, 13) for item in X], wrap=True, fontsize=6)
#     plt.yticks(wrap=True, fontsize=7)
#     plt.tight_layout()
#
#     imgdata = io.BytesIO()
#     fig.savefig(imgdata, format="PDF")
#
#     return imgdata
#
#
# def sort_string_list(X, Y):
#     dict = {}
#     for item in range(len(X)):
#         dict[str(X[item])] = len(str(X[item]))
#     sort_ls = sorted(dict.items(), key=lambda x: x[1], reverse=True)
#
#     new_x_ls = []
#     new_y_ls = []
#     for name, le in sort_ls:
#         new_x_ls.append(name)
#         new_y_ls.append(Y[X.index(name)])
#
#     return new_x_ls, new_y_ls
#
#
# def pie_distribution(data, figsize, colors_list):
#     fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(aspect="equal"))
#     X_old = data["categories"]
#     Y_old = data["values"]
#     X, Y = sort_string_list(X_old, Y_old)
#
#     wedges, texts = ax.pie(Y, wedgeprops=dict(width=0.4), startangle=90)
#     kw = dict(arrowprops=dict(arrowstyle="-"), zorder=0, va="center")
#
#     for i, p in enumerate(wedges):
#         angle = (p.theta2 - p.theta1) / 2.0 + p.theta1
#         y = np.sin(np.deg2rad(angle))
#         x = np.cos(np.deg2rad(angle))
#         horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
#         connectionstyle = f"angle,angleA=0,angleB={angle}"
#         kw["arrowprops"].update({"connectionstyle": connectionstyle})
#         ax.annotate(
#             fill(X[i], 13),
#             xy=(x, y),
#             xytext=(1.15 * np.sign(x), 1.2 * y),
#             horizontalalignment=horizontalalignment,
#             **kw,
#             fontsize=7,
#             wrap=True,
#         )
#     ax.pie(
#         Y,
#         autopct="%2.1f%%",
#         shadow=True,
#         wedgeprops={"width": 0.5},
#         pctdistance=0.7,
#         colors=colors_list[0 : len(X)],
#     )
#
#     ax.set_title("The proportion of labels", fontsize=9)
#     plt.tight_layout()
#
#     imgdata = io.BytesIO()
#     fig.savefig(imgdata, format="PDF")
#     return imgdata
#
#
# # draw tables
# # draw user information table
# def drawUserInfoTable(userinfo_data):
#     t = Table(userinfo_data)
#     t.setStyle(style_dict["userinfo_style"])
#     return t
#
#
# # draw verification result table
# def ResultTable(data_summary):
#     pdf_data = wrap_table(data_summary)
#
#     colwidths_2 = [20, 48, 65, 60, 68, 45, 165]
#
#     # create table using the platypus Table object & set the style
#     tbl_summary = Table(pdf_data, colwidths_2, hAlign="LEFT", repeatRows=1)
#     tbl_summary.setStyle(style_dict["tblstyle"])
#     return tbl_summary
#
#
# def feature_table(data):
#     pdf_data = wrap_table(data)
#     # Build the Table and Style Information
#     colwidths_2 = [30, 80, 300, 70]
#     tableThatSplitsOverPages = Table(pdf_data, colwidths_2, hAlign="LEFT", repeatRows=1)
#     tableThatSplitsOverPages.setStyle(style_dict["tblstyle"])
#
#     return tableThatSplitsOverPages
#
#
# # draw images
# # draw label distribution images (bar & pie)
# def label_distributions(data, colors_list):
#     imgdata = bar_distribution(
#         data=data, figsize=(3.55, 3.2), colors_list=colors_list, x_name="Label"
#     )
#     pi = PdfImage(imgdata)
#
#     imgdata2 = pie_distribution(data=data, figsize=(3, 3.1), colors_list=colors_list)
#     pi2 = PdfImage(imgdata2)
#     return Table([[pi, pi2]], colWidths=[250, 250])  # Table([[pi, pi2]])
#
#
# # draw features distrib=uton images (bar & bar for each row)
# def two_feature_distribution(data1, data2, colors_list, name_list):
#     imgdata = bar_distribution(
#         data=data1, figsize=(3.5, 3.5), colors_list=colors_list, x_name=name_list[0]
#     )
#     pi = PdfImage(imgdata)
#     if data2:
#         imgdata2 = bar_distribution(
#             data=data2, figsize=(3.5, 3.5), colors_list=colors_list, x_name=name_list[1]
#         )
#         pi2 = PdfImage(imgdata2)
#         return Table([[pi, pi2]], colWidths=[250, 250])
#     else:
#         return Table(
#             [
#                 [
#                     pi,
#                 ]
#             ]
#         )
#
#
# # draw features distribution by layout
# def draw_features_images(elements, feature_data):
#     feature_names = list(feature_data.keys())
#     feature_list_len = len(feature_data)
#     for item in range(round(feature_list_len / 2)):
#         name1 = feature_names[item * 2]
#         value1 = feature_data[name1]
#         data1 = {
#             "categories": list(value1.keys()),
#             "values": list(value1.values()),
#         }
#         if feature_list_len % 2 != 0 and item == round(feature_list_len / 2) - 1:
#             elements.append(
#                 two_feature_distribution(
#                     data1=data1,
#                     data2=False,
#                     colors_list=colors_list,
#                     name_list=[
#                         name1,
#                     ],
#                 )
#             )
#         else:
#             name2 = feature_names[item * 2 + 1]
#             value2 = feature_data[name2]
#             data2 = {
#                 "categories": list(value2.keys()),
#                 "values": list(value2.values()),
#             }
#             elements.append(
#                 two_feature_distribution(
#                     data1=data1,
#                     data2=data2,
#                     colors_list=colors_list,
#                     name_list=[name1, name2],
#                 )
#             )
#     return elements
#
#
# # utils for table
# def wrap_table(data):
#     s = getSampleStyleSheet()
#     s = s["Normal"]
#     s.wordWrap = "CJK"
#     s.fontSize = 7
#     s.alignment = TA_CENTER
#     s.textColor = colors.white
#
#     s2 = getSampleStyleSheet()
#     s2 = s2["Normal"]
#     s2.wordWrap = "CJK"
#     s2.fontSize = 7
#     s2.alignment = TA_CENTER
#
#     pdf_data = []
#
#     max_column = 0
#     for item in range(len(data)):
#         if item == 0:
#             data[item].insert(0, "SN")
#         else:
#             data[item].insert(0, str(item))
#         max_column = max(max_column, len(data[item]))
#
#     for key in range(len(data)):
#         if key > 0:  # 内容行（除了表头行）
#             for item_column in range(len(data[key])):
#                 if not data[key][item_column]:
#                     data[key][item_column] = str(
#                         "NULL"
#                     )  # '\n'.join(str(data[key][item_column]) + "--")
#                 else:
#                     data[key][item_column] = str(data[key][item_column])
#
#             pdf_data.append([Paragraph(cell, s2) for cell in data[key]])
#         else:
#             pdf_data.append([Paragraph(cell, s) for cell in data[key]])
#     return pdf_data
#
#
# class PageNumCanvas(canvas.Canvas):
#     def __init__(self, *args, **kwargs):
#         """Constructor"""
#         canvas.Canvas.__init__(self, *args, **kwargs)
#         self.pages = []
#
#     def showPage(self):
#         """
#         On a page break, add information to the list
#         """
#         self.pages.append(dict(self.__dict__))
#         self._startPage()
#
#     def save(self):
#         """
#         Add the page number to each page (page x of y)
#         """
#         page_count = len(self.pages)
#
#         for page in self.pages:
#             self.__dict__.update(page)
#             self.draw_page_number(page_count)
#             canvas.Canvas.showPage(self)
#
#         canvas.Canvas.save(self)
#
#     def draw_page_number(self, page_count):
#         """
#         Add the Header and Footer include page number
#         """
#         # Add the Header(logo image).
#         image_path = "static/rest_framework/img/all.png"
#         img = Image(image_path)
#         img.drawWidth = 45 * (img.imageWidth / img.imageHeight)
#         img.drawHeight = 45
#
#         self.drawImage(
#             image_path, 30, A4[1] - 45, img.drawWidth, img.drawHeight, mask="auto"
#         )
#         self.setStrokeColor(Color(0, 0, 0, alpha=0.5))
#         self.line(10 * mm, A4[1] - 45, A4[0] - 10 * mm, A4[1] - 45)
#
#         # Add the Footer (create time & page info).
#         date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         self.setFillColor(Color(0, 0, 0, alpha=0.5))
#         self.setFont("Arial", 8)
#         self.drawString(30, A4[1] - 810, f"Create Time: {date}")
#
#         self.setFont("Helvetica", 9)
#         self.setStrokeColor(Color(0, 0, 0, alpha=0.5))
#         self.line(10 * mm, 15 * mm, A4[0] - 10 * mm, 15 * mm)
#         self.setFillColor(Color(0, 0, 0, alpha=0.5))
#         self.drawCentredString(
#             A4[0] / 2, 10 * mm, "Page %d of %d" % (self._pageNumber, page_count)
#         )
