from itertools import combinations

import matplotlib
import matplotlib.pyplot as plt

from sql_helper.SQLSearch import SQLSearch

matplotlib.use("PDF")
import io
import os
from math import pi, ceil
import numpy as np
from datetime import datetime, timedelta

from textwrap import fill
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    SimpleDocTemplate,
    Image,
    Paragraph,
    TableStyle,
    Table,
    Spacer, PageBreak,
)

IMG_FOLDER_PATH = "static/rest_framework/img"  # 'images'
blue_image_path = os.path.join(
    os.getcwd(), os.path.join(IMG_FOLDER_PATH, "bluebar.png")
)
logo_image_path = os.path.join(os.getcwd(), os.path.join(IMG_FOLDER_PATH, "all.png"))


FONTS_FOLDER_PATH = "static/rest_framework/fonts"  # 'fonts'
pdfmetrics.registerFont(
    TTFont(
        "Calibri",
        os.path.join(os.getcwd(), os.path.join(FONTS_FOLDER_PATH, "calibri.ttf")),
    )
)
pdfmetrics.registerFont(
    TTFont(
        "Calibri-Italic",
        os.path.join(os.getcwd(), os.path.join(FONTS_FOLDER_PATH, "calibrii.ttf")),
    )
)
pdfmetrics.registerFont(
    TTFont(
        "Calibri-Bold",
        os.path.join(os.getcwd(), os.path.join(FONTS_FOLDER_PATH, "calibrib.ttf")),
    )
)
pdfmetrics.registerFont(
    TTFont(
        "Calibri-Bold-Italic",
        os.path.join(os.getcwd(), os.path.join(FONTS_FOLDER_PATH, "calibriz.ttf")),
    )
)


pdfmetrics.registerFontFamily(
    "Calibri",
    normal="Calibri",
    italic="Calibri-Italic",
    bold="Calibri-Bold",
    boldItalic="Calibri-Bold-Italic",
)

# Define colors for bar chart
# bar_colors = [
#     "springgreen",
#     "cyan",
#     "deepskyblue",
#     "magenta",
#     "violet",
#     "lightpink",
#     "salmon",
#     "gold",
#     "orange",
#     "orangered",
# ]

# Define colors for pie chart
pie_colors = [
    "#5470c6",
    "#91cc75",
    "#fac858",
    "#ee6666",
    "#73c0de",
    "#3ba272",
    "lightpink",
]

# Define Paragraph or Table style
styles = getSampleStyleSheet()
style_dict = {
    "title": ParagraphStyle(
        name="Title",
        fontName="Calibri",
        parent=styles["Title"],
        fontSize=24,
        leading=16,
        alignment=1,
        spaceAfter=20,
    ),
    "heading1": ParagraphStyle(
        name="heading1",
        fontName="Calibri",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=4,
        firstLineIndent=0,
    ),
    "heading2": ParagraphStyle(
        "heading2",
        fontName="Calibri",
        parent=styles["Heading3"],
        textColor="#00b0f0",
        fontSize=18,
        spacebefore=0,
        bulletFontSize=12,
        bulletFontName="Symbol",
        bulletText="•",
    ),
    "no_order_list": ParagraphStyle(
        "no_order_list",
        fontName="Calibri",
        parent=styles["Heading3"],
        textColor=colors.black,
        fontSize=14,
        leading=4,
        spacebefore=0,
        bulletFontSize=8,
        bulletFontName="Symbol",
        bulletText="•",
    ),
    "normal": ParagraphStyle(
        name="normal",
        fontName="Calibri",
        parent=styles["Normal"],
        fontSize=14,
        leading=14,
        spaceAfter=14,
    ),
    "table_normal": ParagraphStyle(
        name="table_normal",
        fontName="Calibri",
        parent=styles["Normal"],
        fontSize=12,
        leading=12,
    ),
    "verification_tblstyle": TableStyle(
        [
            ("LINEABOVE", (0, 0), (-1, 0), 1, colors.HexColor("#7C7C7C")),
            ("LINEBELOW", (0, 0), (-1, 0), 1, colors.HexColor("#A5A5A5")),
            ("LINEBELOW", (0, -1), (-1, -1), 1, colors.HexColor("#A5A5A5")),
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            (
                "ROWBACKGROUNDS",
                (0, 0),
                (-1, -1),
                (colors.HexColor("#FFFFFF"), colors.HexColor("#EDEDED")),
            ),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("ALIGN", (0, 1), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    ),
}


class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        """
        Add the Header and Footer include page number
        """
        # Add the Header(logo image).
        image_path = logo_image_path
        img = Image(image_path)
        img.drawWidth = 45 * (img.imageWidth / img.imageHeight)
        img.drawHeight = 45

        self.drawImage(
            image_path, 30, A4[1] - 45, img.drawWidth, img.drawHeight, mask="auto"
        )
        self.setStrokeColor(Color(0, 0, 0, alpha=0.5))
        self.line(10 * mm, A4[1] - 45, A4[0] - 10 * mm, A4[1] - 45)

        # Add the Footer (create time & page info).
        current_time = str(
            (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        )
        self.setFillColor(Color(0, 0, 0, alpha=0.5))
        self.setFont("Calibri", 8)
        self.drawString(30, A4[1] - 810, f"Create Time: {current_time}")

        self.setFont("Calibri", 9)
        self.setStrokeColor(Color(0, 0, 0, alpha=0.5))
        self.line(10 * mm, 15 * mm, A4[0] - 10 * mm, 15 * mm)
        self.setFillColor(Color(0, 0, 0, alpha=0.5))
        self.drawCentredString(
            A4[0] / 2, 10 * mm, "Page %d of %d" % (self._pageNumber, page_count)
        )


class PdfImage(Flowable):
    """PdfImage wraps the page from a PDF file as a Flowable
    which can be included into a ReportLab Platypus document.
    Based on the vectorpdf extension in rst2pdf (http://code.google.com/p/rst2pdf/)"""

    def __init__(self, filename_or_object, width=None, height=None, kind="direct"):
        from reportlab.lib.units import inch

        # If using StringIO buffer, set pointer to beginning
        if hasattr(filename_or_object, "read"):
            filename_or_object.seek(0)
        page = PdfReader(filename_or_object, decompress=False).pages[0]
        self.xobj = pagexobj(page)
        self.imageWidth = width
        self.imageHeight = height
        x1, y1, x2, y2 = self.xobj.BBox

        self._w, self._h = x2 - x1, y2 - y1
        if not self.imageWidth:
            self.imageWidth = self._w
        if not self.imageHeight:
            self.imageHeight = self._h
        self.__ratio = float(self.imageWidth) / self.imageHeight
        if kind in ["direct", "absolute"] or width is None or height is None:
            self.drawWidth = width or self.imageWidth
            self.drawHeight = height or self.imageHeight
        elif kind in ["bound", "proportional"]:
            factor = min(float(width) / self._w, float(height) / self._h)
            self.drawWidth = self._w * factor
            self.drawHeight = self._h * factor

    def wrap(self, aW, aH):
        return self.drawWidth, self.drawHeight

    def drawOn(self, canv, x, y, _sW=0):
        if _sW > 0 and hasattr(self, "hAlign"):
            a = self.hAlign
            if a in ("CENTER", "CENTRE", TA_CENTER):
                x += 0.5 * _sW
            elif a in ("RIGHT", TA_RIGHT):
                x += _sW
            elif a not in ("LEFT", TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))

        xobj = self.xobj
        xobj_name = makerl(canv._doc, xobj)

        xscale = self.drawWidth / self._w
        yscale = self.drawHeight / self._h

        x -= xobj.BBox[0] * xscale
        y -= xobj.BBox[1] * yscale

        canv.saveState()
        canv.translate(x, y)
        canv.scale(xscale, yscale)
        canv.doForm(xobj_name)
        canv.restoreState()


class PdfImage2(Flowable):
    def __init__(self, img_data, width=200, height=200):
        self.img_width = width
        self.img_height = height
        self.img_data = img_data

    def wrap(self, width, height):
        return self.img_width, self.img_height

    def drawOn(self, canv, x, y, _sW=0):
        if _sW > 0 and hasattr(self, "hAlign"):
            a = self.hAlign
            if a in ("CENTER", "CENTRE", TA_CENTER):
                x += 0.5 * _sW
            elif a in ("RIGHT", TA_RIGHT):
                x += _sW
            elif a not in ("LEFT", TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))
        canv.saveState()
        canv.drawImage(self.img_data, x, y, self.img_width, self.img_height)
        canv.restoreState()

# create reports
# create report for data verification
def data_verification_report(filename, task_id, data_userinfo, data_result):
    elements = [Paragraph("<b>Data Verification Report Good Man Nice Man Cool Man</b>", style_dict["title"])]
    elements.append(Spacer(1, 3 * mm))

    if data_userinfo:
        # 蓝色条
        image_path = blue_image_path
        img = Image(image_path, hAlign="LEFT")
        img.drawWidth = 10 * (img.imageWidth / img.imageHeight)
        img.drawHeight = 10

        # Basic Information
        ptext = "<b>Basic Information</b>"
        elements.append(Paragraph(ptext, style=style_dict["heading1"]))
        elements.append(img)
        for item in data_userinfo:
            ptext = f"""{item[0]}: {item[1]}"""
            elements.append(Paragraph(ptext, style=style_dict["no_order_list"]))
        elements.append(Spacer(1, 8 * mm))

        # Test Result
        ptext = "<b>Test Result</b>"
        elements.append(Paragraph(ptext, style=style_dict["heading1"]))
        elements.append(img)
        elements.append(Spacer(1, 3 * mm))
        if data_result:
            pdf_data = verification_table(data_result)
            colwidths_2 = [20, 48, 65, 60, 68, 45, 165]
            tbl_summary = Table(pdf_data, colwidths_2, hAlign="LEFT", repeatRows=1,rowHeights=12 * mm)
            tbl_summary.setStyle(style_dict["verification_tblstyle"])
            elements.append(tbl_summary)
        else:
            ptext = "The verification results can be obtained only after the data validation task is established"
            elements.append(Paragraph(ptext, style=style_dict["normal"],))
        elements.append(Spacer(1, 8 * mm))
        elements.append(PageBreak())

        # Appendix
        ptext = "<b>Appendix</b>"
        elements.append(Paragraph(ptext, style=style_dict["heading1"]))
        elements.append(img)

        ptext = "<b><i>Dataset Summary</i></b>"
        elements.append(Paragraph(ptext, style=style_dict["heading2"]))
        elements.append(Spacer(1, 3 * mm))

        # 1.1
        ptext = "<b># Samples & Labels distribution</b>"
        elements.append(Paragraph(ptext, style=style_dict["normal"]))

        dataset_info, label_data = get_dataset_info(task_id)
        samples_number = dataset_info["count"]
        version_number = dataset_info["version"]
        dataset_description = dataset_info["table_description"]

        if label_data:
            dataset_class = label_data["categories"]
            dataset_class_no = len(dataset_class)

            ptext = f"""There are <a color='#c00000'><b>{samples_number}</b></a> samples in datasets <a color='#c00000'><b>{dataset_description}</b></a> with version <a color='#c00000'><b>{version_number}</b></a> in all, including <a color='#c00000'><b>{dataset_class_no}</b></a> categories ({dataset_class}). """
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
            ptext = "The related test results are as follows:"
            elements.append(Paragraph(ptext, style=style_dict["normal"]))

            ptext = "<a color='#c00000'><b>Fig1. The distribution & proportion of labels</b></a>"
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
            imgdata = verificatrion_pie_distribution(data=label_data, figsize=(5, 3.8), colors=pie_colors)
            pi_item = PdfImage(imgdata)
            elements.append(Table([[pi_item]]))
        else:
            ptext = f"""There are <a color='#c00000'><b>{samples_number}</b></a> samples in datasets <a color='#c00000'><b>{dataset_description}</b></a> with version <a color='#c00000'><b>{version_number}</b></a> in all. """
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
            ptext = f"""Only one field is allowed to be a label, so the distribution of label categories on the dataset cannot be displayed."""
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
        elements.append(Spacer(1, 3 * mm))

        # 1.2
        ptext = "<b># Feature name list</b>"
        elements.append(Paragraph(ptext, style=style_dict["normal"]))
        feature_name_list, feature_data = get_feature_names(
            table_name=dataset_info["table_name"],
            version=dataset_info["version"],
            table_id=dataset_info["table_id"],
        )
        if feature_name_list:
            features_for_heatmap = list(feature_data.keys())

            ptext = f"""From the metadata of the dataset, there are <a color='#c00000'><b>{len(features_for_heatmap)}</b></a> features whose number of distinct values within the range of[2,10]."""
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
            ptext = "The related test results are as follows:"
            elements.append(Paragraph(ptext, style=style_dict["normal"]))

            ptext = "<a color='#c00000'><b>Fig1. Feature name list</b></a>"
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
            pdf_data = verification_table(feature_name_list)
            colwidths = [30, 80, 300, 70]
            tableThatSplitsOverPages = Table(pdf_data, colwidths, hAlign="LEFT", repeatRows=1)
            tableThatSplitsOverPages.setStyle(style_dict["verification_tblstyle"])
            elements.append(tableThatSplitsOverPages)
        else:
            ptext = f"""From the metadata of the dataset, we can't find the features whose number of distinct value within range [2,10])"""
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
        elements.append(Spacer(1, 3 * mm))

        # 1.3
        ptext = "<b># Feature distribution display</b>"
        elements.append(Paragraph(ptext, style=style_dict["normal"]))
        if feature_data:
            ptext = "The related test results are as follows:"
            elements.append(Paragraph(ptext, style=style_dict["normal"]))

            feature_names = list(feature_data.keys())
            for index in range(0, len(feature_data)):
                x_name = feature_names[index]
                values = feature_data[x_name]

                ptext = f"""<a color='#c00000'><b>Fig{index + 1}. The distribution & proportion of {feature_names[index]}</b></a>"""
                elements.append(Paragraph(ptext, style=style_dict["normal"]))

                data = {
                    "categories": list(values.keys()),
                    "values": list(values.values())
                }
                imgdata = verificatrion_pie_distribution(data=data, figsize=(5, 3.8), colors=pie_colors)
                pi_item = PdfImage(imgdata)
                elements.append(Table([[pi_item]]))
        else:
            ptext = "As there is no feature whose number of distinct values within the range [2,10]), the distribution chart cannot be displayed."
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
        elements.append(Spacer(1, 3 * mm))

        # 1.4
        ptext = "<b># Double ODD cross coverage heatmap display</b>"
        elements.append(Paragraph(ptext, style=style_dict["normal"]))
        if (not feature_data) or (len(list(feature_data.keys())) < 2):
            ptext = "As the number of available feature is less than two, the heatmap of odd cross coverage cannot be displayed."
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
        else:
            features_for_heatmap = list(feature_data.keys())
            feature_text = ", ".join([item for item in features_for_heatmap if item is not None])
            ptext = f"""In this section, ODD cross coverage statistics are conducted between the <a color='#c00000'><b>{len(features_for_heatmap)}</b></a> features in pairs."""
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
            ptext = f"""For the features <a color='#c00000'><b>{feature_text}</b></a>, the following <a color='#c00000'><b>{len(list(combinations(features_for_heatmap, 2)))}</b></a> heat maps are generated."""
            elements.append(Paragraph(ptext, style=style_dict["normal"]))
            ptext = "The related test results are as follows:"
            elements.append(Paragraph(ptext, style=style_dict["normal"]))

            table_name = dataset_info["table_name"]
            version = dataset_info["version"]
            items = list(feature_data.keys())
            com_list = list(combinations(items, 2))

            for index in range(0, len(com_list)):
                com = com_list[index]
                data = prepare_heatmap_data(table_name, version, feature_data, com)
                features = data["combination"]
                ptext = f"""<a color='#c00000'><b>Fig{index + 1}. coverage of {features[0]} and {features[1]}</b></a>"""
                elements.append(Paragraph(ptext, style=style_dict["normal"]))
                pi_item = heatmap_for_features(data)
                elements.append(Table([[pi_item]], [200], hAlign="CENTER"))
        elements.append(Spacer(1, 8 * mm))

        # 2
        ptext = "<b><i>Data coverage details within scenarios from data requirements</i></b>"
        elements.append(Paragraph(ptext, style=style_dict["heading2"]))

        # 2.1
        ptext = "<b># ODD parameters list</b>"
        elements.append(Paragraph(ptext, style=style_dict["normal"]))

        # 2.2
        ptext = "<b># ODD data coverage display</b>"
        elements.append(Paragraph(ptext, style=style_dict["normal"]))
    else:
        elements.append(Paragraph("Can not find any information for this data verification task.", style=style_dict["normal"],))

    doc = SimpleDocTemplate(filename,)
    doc.build(elements, canvasmaker=PageNumCanvas)


def get_dataset_info(task_id):
    sql_helper = SQLSearch()
    str_sql = f"""
    SELECT B.`table_name_mysql`, B.`table_description`, A.`version`, A.`table_id`
    FROM prosafeAI_data_verification_task A
    INNER JOIN prosafeAI_table B ON B.id=A.table_id
    WHERE B.table_type='metadata' and A.id={task_id}
    """
    data = sql_helper.search(str_sql)
    table_name = data[0]["table_name_mysql"]
    version = data[0]["version"]
    table_id = data[0]["table_id"]

    str_sql2 = f"""
    SELECT count(*) as count from {table_name} where  data_version={version}
    """
    data2 = sql_helper.search(str_sql2)
    dataset_info = {
        "table_description": data[0]["table_description"],
        "table_name": table_name,
        "version": version,
        "count": data2[0]["count"],
        "table_id": table_id,
    }

    str_sql3_1 = f"""
    SELECT count(field_name) as count FROM prosafeAI_field where table_id = {table_id} and field_category = 'label'
    """
    label_count = sql_helper.search(str_sql3_1)[0]["count"]

    if label_count == 1:
        str_sql3 = f"""
        SELECT field_name FROM prosafeAI_field where table_id = {table_id} and field_category = 'label'
        """
        label_name = sql_helper.search(str_sql3)[0]["field_name"]

        str_sql4 = f"""
        SELECT {label_name}, count(id) as VALUE FROM {table_name} WHERE data_version={version} GROUP BY {label_name}
        """

        label_name_list = sql_helper.search(str_sql4)

        label_data = {}
        class_list = []
        value_list = []
        for item in range(len(label_name_list)):
            class_list.append(label_name_list[item][label_name])
            value_list.append(label_name_list[item]["VALUE"])

        label_data["categories"] = class_list
        label_data["values"] = value_list

    else:
        label_data = False

    return dataset_info, label_data

# def verification_bar_distribution(data, figsize, colors, title=None):
#     X = data["categories"]
#     Y = data["values"]
#
#     my_colors = colors[0: len(X)]
#
#     fig, ax = plt.subplots(figsize=figsize)
#
#     ax_cur = ax
#     ax.set_axisbelow(True)
#     ax_cur.grid(ls="-", axis="y", color="#C0C0C0", alpha=0.3)
#
#     p = ax_cur.bar(X, Y, color=my_colors)
#     if title:
#         ax.set_title(title, fontdict={"size": 13, "family": ["Calibri"], "weight": "bold"})
#
#     ax_cur.spines["top"].set_visible(False)
#     ax_cur.spines["right"].set_visible(False)
#     ax.bar_label(p, fontsize=8)
#
#     plt.xticks(arange(len(X)), [fill(item, 13) for item in X], wrap=True, fontsize=8)
#     plt.yticks(wrap=True, fontsize=8)
#     plt.tight_layout()
#
#     imgdata = io.BytesIO()
#     fig.savefig(imgdata, format="PDF")
#     return imgdata


def verificatrion_pie_distribution(data, figsize, colors, title=None):
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(aspect="equal"))

    X = data["categories"]
    Y = data["values"]

    my_colors = colors

    wedges, texts = ax.pie(
        Y,
        wedgeprops=dict(width=0.6),
        startangle=90.1,
        pctdistance=0.7,
        colors=colors[0: len(X)],
    )

    kw = dict(arrowprops=dict(arrowstyle="-"), zorder=0, va="center")

    string_length = sum(len(x) for x in X)
    row_num = ceil(string_length / 30)

    if title:
        annotate_fontsize = 5
        pie_textprops_fontsize = 5
        legend_bbox_to_anchor = (0.5, 1)
        if row_num > 1:
            legend_ncol = ceil(len(X) / row_num)
            legend_prop_size = 6
        else:
            legend_ncol = len(X)
            legend_prop_size = 7
    else:
        annotate_fontsize = 7
        pie_textprops_fontsize = 7
        legend_ncol = len(X)
        legend_bbox_to_anchor = (0.5, 1.02)
        legend_prop_size = 7
    for i, p in enumerate(wedges):
        angle = (p.theta2 - p.theta1) / 2.0 + p.theta1
        y = np.sin(np.deg2rad(angle))
        x = np.cos(np.deg2rad(angle))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={angle}"
        kw["arrowprops"].update(
            {"connectionstyle": connectionstyle, "color": colors[i]}
        )
        ax.annotate(
            "{:.1f}%".format(
                Y[i] * 100 / sum(Y),
            ),
            xy=(x, y),
            xytext=(1.15 * np.sign(x), 1.15 * y),
            horizontalalignment=horizontalalignment,
            **kw,
            fontsize=annotate_fontsize,
            wrap=True,
        )
    index = 0
    def label_value(pct):
        nonlocal index
        value = Y[index]
        index += 1
        return value
    ax.pie(
        Y,
        # autopct=lambda pct: "{:d}".format(ceil(pct / 100 * sum(Y))),
        autopct=label_value,
        shadow=False,
        startangle=90.1,
        wedgeprops={"width": 0.6},
        textprops={"fontsize": pie_textprops_fontsize},
        pctdistance=0.7,
        colors=my_colors[0: len(X)],
    )

    ax.legend(
        wedges,
        X,
        ncol=legend_ncol,
        loc="lower center",
        bbox_to_anchor=legend_bbox_to_anchor,
        prop={"size": legend_prop_size},
        frameon=False,
    )

    if title:
        ax.set_title(title, loc="left", fontdict={"size": 11, "family": ["Calibri"], "weight": "bold"}, y=1.15, )

    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="PDF")
    return imgdata

def get_feature_names(table_name, version, table_id):
    sql_helper = SQLSearch()
    str_sql = f"""
    SELECT field_name from prosafeAI_field where table_id ={table_id}
    """
    names_tmp = sql_helper.search(str_sql)

    names = [names_tmp[item]["field_name"] for item in range(len(names_tmp))]

    str_begin = "select "
    for name_item in range(len(names)):
        str_slice = f"""count(distinct({names[name_item]})) as {names[name_item]},"""
        str_begin += str_slice
    new_str = str_begin.rstrip(",")
    last_str = f""" 
     from {table_name} where data_version={version}
    """
    str_sql2 = new_str + last_str
    counts = sql_helper.search(str_sql2)[0]

    name_value_dict = dict(filter(lambda x: x[1] > 1 and x[1] < 10, counts.items()))

    if name_value_dict:
        name_list = list(name_value_dict.keys())
        value_list = list(name_value_dict.values())

        new_name_str = ", ".join(name_list)

        str_sql_temp = "select " + name_list[0] + " from a "
        for item_name in range(len(name_list)):
            temp_slice = f"""
            UNION select {name_list[item_name]} from a
            """
            str_sql_temp += temp_slice

        str_sql3 = f"""
        WITH a AS 
        (SELECT {new_name_str} from {table_name} where data_version={version}) 
        {str_sql_temp}
        """
        feature_names = sql_helper.search(str_sql3)

        feature_values = [
            feature_names[item][name_list[0]] for item in range(len(feature_names))
        ]
        flag = 0
        feature_name_list = [["Feature Name", "Feature Values", "No. of Values"]]
        for item in range(len(value_list)):
            a = str(feature_values[flag : flag + value_list[item]])
            flag += value_list[item]
            feature_name_list.append([name_list[item], a, value_list[item]])

        feature_data = {}
        for item in range(len(name_list)):
            str_sql4 = f"""
            select {name_list[item]}, count(id) as value from {table_name} where data_version={version} group by {name_list[item]}
            """
            data = sql_helper.search(str_sql4)

            data2 = {}
            for x in range(len(data)):
                data2[data[x][name_list[item]]] = data[x]["value"]

            feature_data[name_list[item]] = data2

    else:
        feature_name_list = False
        feature_data = False

    return feature_name_list, feature_data



def verification_table(data):
    s = getSampleStyleSheet()
    s = s["Normal"]
    s.wordWrap = "CJK"
    s.fontSize = 7
    s.alignment = TA_CENTER
    s.textColor = colors.black

    s2 = getSampleStyleSheet()
    s2 = s2["Normal"]
    s2.wordWrap = "CJK"
    s2.fontSize = 7
    s2.alignment = TA_CENTER

    pdf_data = []

    max_column = 0
    for item in range(len(data)):
        if item == 0:
            data[item].insert(0, "SN")
        else:
            data[item].insert(0, str(item))
        max_column = max(max_column, len(data[item]))

    for key in range(len(data)):
        if key > 0:  # 内容行（除了表头行）
            for item_column in range(len(data[key])):
                if not data[key][item_column]:
                    data[key][item_column] = str("NULL")
                else:
                    data[key][item_column] = str(data[key][item_column])
            pdf_data.append([Paragraph(cell, s2) for cell in data[key]])
        else:
            pdf_data.append([Paragraph(f"""<b>{" ".join(cell.split("_")).title()}</b>""", s) if cell != "SN" else Paragraph(f"""<b>{cell}</b>""", s) for cell in data[key]])
    return pdf_data

def prepare_heatmap_data(table_name, version, feature_data, com):
    sql_helper = SQLSearch()
    feature_value_1 = list(feature_data[com[0]].keys())  # ['no snow', 'light snow']
    feature_value_2 = list(
        feature_data[com[1]].keys()
    )  # ['cloudy', 'sunny', 'partly sunny']

    str_sql_com = f"""
    SELECT {com[0]}, {com[1]}, count(id) as count FROM {table_name} WHERE data_version={version} GROUP BY {com[0]}, {com[1]}
    """
    feature_values_sql = sql_helper.search(str_sql_com)
    data_array = np.zeros([len(feature_value_1), len(feature_value_2)], dtype=np.int32)

    for item_value in range(len(feature_values_sql)):
        x = feature_value_1.index(feature_values_sql[item_value][com[0]])
        y = feature_value_2.index(feature_values_sql[item_value][com[1]])
        data_array[x][y] = feature_values_sql[item_value]["count"]

    if len(feature_value_1) > len(feature_value_2):
        data = {
            "data": data_array.T,
            "feature_value_1": feature_value_2,
            "feature_value_2": feature_value_1,
            "combination": [com[1], com[0]],
        }

    else:
        data = {
            "data": data_array,
            "feature_value_1": feature_value_1,
            "feature_value_2": feature_value_2,
            "combination": com,
        }
    return data
def heatmap_for_features(data, title=None):
    data_info = data["data"]
    feature_value_1 = data["feature_value_1"]
    feature_value_2 = data["feature_value_2"]
    features = data["combination"]

    fig, ax = plt.subplots(dpi=800)

    im, cbar = heatmap(
        data_info,
        features,
        feature_value_1,
        feature_value_2,
        ax=ax,
        # cmap="YlGn",
        cmap="OrRd",
        # cbarlabel="# of samples",
    )
    fig.tight_layout()
    if title:
        ax.set_title(title)
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="png")
    imgdata.seek(0)
    image = ImageReader(imgdata)
    img = PdfImage2(image, width=200, height=150)
    return img

def heatmap(
    data,
    features,
    row_labels,
    col_labels,
    ax=None,
    cbar_kw=None,
    cbarlabel="",
    **kwargs,
):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()
    if cbar_kw is None:
        cbar_kw = {}
    # Plot the heatmap
    im = ax.imshow(data, **kwargs)
    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.023, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    # plt.xticks(arange(len(X)), [fill(item, 13) for item in X], wrap=True, fontsize=6, labels=col_labels)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(
        np.arange(data.shape[1]), [fill(item, 10) for item in col_labels], wrap=True
    )
    ax.set_yticks(
        np.arange(data.shape[0]), [fill(item, 10) for item in row_labels], wrap=True
    )
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center", rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), rotation=0, ha="right", rotation_mode="anchor")
    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)
    ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor=True)
    ax.set_xlabel(f""" {features[1]} """)
    ax.set_ylabel(f""" {features[0]} """)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    # raw_ratio = 1.5
    # aspect_ratio = forceAspect(ax, aspect=raw_ratio)
    return im, cbar
