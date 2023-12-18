import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("PDF")

from textwrap import fill
import io
import os
from math import pi, ceil
import numpy as np
from numpy import arange
from datetime import datetime, timedelta
import zipfile
import shutil

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
    Spacer,
)


# blue_image_path = os.path.join(os.getcwd(), 'static/rest_framework/img/bluebar.png')
# logo_image_path = os.path.join(os.getcwd(), 'static/rest_framework/img/all.png')

# pdfmetrics.registerFont(TTFont('Calibri', os.path.join(os.getcwd(), 'static/rest_framework/fonts/calibri.ttf')))
# pdfmetrics.registerFont(TTFont('Calibri-Italic', os.path.join(os.getcwd(), 'static/rest_framework/fonts/calibrii.ttf')))
# pdfmetrics.registerFont(TTFont('Calibri-Bold', os.path.join(os.getcwd(), 'static/rest_framework/fonts/calibrib.ttf')))
# pdfmetrics.registerFont(TTFont('Calibri-Bold-Italic', os.path.join(os.getcwd(), 'static/rest_framework/fonts/calibriz.ttf')))


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
bar_colors = [
    "springgreen",
    "cyan",
    "deepskyblue",
    "magenta",
    "violet",
    "lightpink",
    "salmon",
    "gold",
    "orange",
    "orangered",
]

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
    "no_order_list_robustness": ParagraphStyle(
        "no_order_list_robustness",
        fontName="Calibri",
        parent=styles["Heading3"],
        textColor=colors.black,
        fontSize=12,
        leading=16,
        spacebefore=0,
        bulletFontSize=8,
        bulletFontName="Symbol",
        bulletText="•",
    ),
    "metrics_name": ParagraphStyle(
        name="metrics_name",
        fontName="Calibri",
        parent=styles["Normal"],
        fontSize=12,
        leading=8,
        spaceBefore=4,
        spaceAfter=4,
        firstLineIndent=12,
    ),
    "metrics_method": ParagraphStyle(
        name="metrics_method", fontName="Calibri", parent=styles["Normal"], fontSize=11
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
    "robustness_table_normal": ParagraphStyle(
        name="robustness_table_normal",
        fontName="Calibri",
        parent=styles["Normal"],
        fontSize=14,
        leading=14,
    ),
    "robustness_table_center": ParagraphStyle(
        name="robustness_table_center",
        fontName="Calibri",
        parent=styles["Normal"],
        fontSize=14,
        leading=14,
        alignment=TA_CENTER,
    ),
    "conclusion_normal": ParagraphStyle(
        name="conclusion_normal",
        fontName="Calibri",
        parent=styles["Normal"],
        fontSize=14,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=8,
        firstLineIndent=0,
    ),
    "attack_table_center": ParagraphStyle(
        name="attack_table_center",
        fontName="Calibri",
        parent=styles["Normal"],
        fontSize=8,
        leading=8,
        alignment=TA_CENTER,
    ),
    # Define table style
    "tblstyle": TableStyle(
        [
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.white),
            ("BOX", (0, 0), (-1, -1), 0.25, colors.white),
            ("FONTSIZE", (0, 0), (-1, 0), 7),
            ("FONTSIZE", (0, 1), (-1, -1), 7),
            ("TEXTFONT", (0, 0), (-1, 0), "Calibri-Bold"),
            ("TEXTFONT", (0, 1), (0, -1), "Calibri-Bold"),
            ("TEXTFONT", (0, 1), (-1, -1), "Calibri"),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            (
                "ROWBACKGROUNDS",
                (0, 0),
                (-1, -1),
                (colors.HexColor("#e8e9ec"), colors.HexColor("#CED1D6")),
            ),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3A5675")),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("ALIGN", (0, 1), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    ),
    "feature_metrics_tblstyle": TableStyle(
        [
            ("LINEABOVE", (0, 0), (-1, 0), 2.5, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
            ("LINEBELOW", (0, -1), (-1, -1), 2.5, colors.black),
            ("TEXTFONT", (0, 0), (-1, -1), "Calibri"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    ),
    "metrics_tblstyle": TableStyle(
        [
            ("TEXTFONT", (0, 0), (-1, -1), "Calibri"),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("BOTTOMPADDING", (2, 0), (2, 0), 5 * mm),
            ("BOTTOMPADDING", (4, 0), (4, 0), 5 * mm),
            ("BOTTOMPADDING", (6, 0), (6, 0), 5 * mm),
            ("ALIGN", (0, 0), (0, 0), "CENTER"),
            ("ALIGN", (2, 0), (-1, 0), "LEFT"),
            ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
            ("VALIGN", (2, 0), (-1, 0), "BOTTOM"),
        ]
    ),
    "conclusion_tblstyle": TableStyle(
        [
            ("TEXTFONT", (0, 0), (-1, -1), "Calibri"),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#D3D3D3")]),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]
    ),
    "tblstyle_list": [
        ("LINEABOVE", (0, 0), (-1, 0), 1.5, "#545454"),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, "#545454"),
        ("LINEBELOW", (0, -1), (-1, -1), 1.5, "#545454"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("FONTSIZE", (0, 1), (-1, -1), 11),
        ("TEXTFONT", (0, 0), (-1, -1), "Calibri"),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("LEFTPADDING", (0, 0), (-1, -1), 1),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
        (
            "ROWBACKGROUNDS",
            (0, 0),
            (-1, -1),
            (colors.HexColor("#FFFFFF"), colors.HexColor("#e8e9ec")),
        ),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ],
    "attack_tblstyle_new_list": [
        ("LINEABOVE", (0, 0), (-1, 0), 1.5, "#545454"),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, "#545454"),
        ("LINEBELOW", (0, -1), (-1, -1), 1.5, "#545454"),
        ("TEXTFONT", (0, 0), (-1, -1), "Calibri"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        (
            "ROWBACKGROUNDS",
            (0, 0),
            (-1, -1),
            (colors.HexColor("#FFFFFF"), colors.HexColor("#D3D3D3")),
        ),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ],
    # "attack_tblstyle_new_list": [
    #     ('LINEABOVE', (0, 1), (-1, 1), 1.5, '#545454'),
    #     ('LINEBELOW', (0, 1), (-1, 1), 1.5, '#545454'),
    #     ('LINEBELOW', (0, -1), (-1, -1), 1.5, '#545454'),
    #     ('TEXTFONT', (0, 0), (-1, -1), 'Calibri'),
    #     ('FONTSIZE', (0, 0), (-1, -1), 7),
    #     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    #     ('ROWBACKGROUNDS', (0, 1), (-1, -1), (colors.HexColor('#FFFFFF'), colors.HexColor('#D3D3D3'))),
    #     ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
    #     ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    #     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    # ],
}


def wrap_table(data):
    s = getSampleStyleSheet()
    s = s["Normal"]
    s.wordWrap = "CJK"
    s.fontSize = 7
    s.alignment = TA_CENTER
    s.textColor = colors.white

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

    for key in range(0, len(data)):
        if key > 0:
            if data[key][max_column - 1]:
                data[key][max_column - 1] = "\n".join(str(data[key][max_column - 1]))
            pdf_data.append([Paragraph(cell, s2) for cell in data[key]])
        else:
            pdf_data.append([Paragraph(cell, s) for cell in data[key]])
    return pdf_data


row_names = [
    "Accuracy",
    "Accuracy (Balanced)",
    "Precision (Macro)",
    "Precision (Micro)",
    "Precision (Weighted)",
    "Recall (Macro)",
    "Recall (Micro)",
    "Recall (Weighted)",
    "F1-score (Macro)",
    "F1-score (Micro)",
    "F1-score (Weighted)",
]

row_list = [
    "total*accuracy",
    "balance*accuracy",
    "macro*precision",
    "micro*precision",
    "weighted*precision",
    "macro*recall",
    "micro*recall",
    "weighted*recall",
    "macro*f1score",
    "micro*f1score",
    "weighted*f1score",
]

row_names_new = [
    Paragraph(f"""<b>{str(row_names[item])}</b>""", style=style_dict["table_normal"])
    for item in range(len(row_names))
]
percent = [Paragraph(f"""<b> (%) </b>""")]


def metrics_table(slice_data):
    feature_values = slice_data["values"]
    feature_values_new = [
        Paragraph(
            f"""<b>{str(feature_values[item])}</b>""", style=style_dict["table_normal"]
        )
        for item in range(len(feature_values))
    ]

    Basic_table = [percent + feature_values_new]
    for item in range(len(row_names)):
        value_list = []
        for item_value in range(len(feature_values)):
            row_name_item = row_list[item]
            metric_value = round(
                slice_data[feature_values[item_value]][row_name_item] * 100, 1
            )
            if metric_value == 100.0:
                metric_value = 100
            value_list.append(metric_value)
        if len(value_list) > 1:
            max_index = [
                i for i, val in enumerate(value_list) if val == max(value_list)
            ]
            other_index = list(set(range(len(value_list))).difference(max_index))

            for value_item in max_index:
                value_list[value_item] = Paragraph(
                    f"""<b>{value_list[value_item]}</b>""",
                    style=style_dict["table_normal"],
                )
            for value_item in other_index:
                value_list[value_item] = Paragraph(
                    f"""{value_list[value_item]}""", style=style_dict["table_normal"]
                )
        else:
            for value_item in range(len(value_list)):
                value_list[value_item] = Paragraph(
                    f"""{value_list[value_item]}""", style=style_dict["table_normal"]
                )

        item_list = [row_names_new[item]] + value_list
        Basic_table.append(item_list)
    return Basic_table


def Basic_Metrics_Table(data):
    number = len(data[0]) - 1
    if number != 5:
        col_wid = 300 / number
        colwidths_tmp = [150] + list((np.ones(number) * col_wid))
        colwidths = list(map(lambda x: int(x), colwidths_tmp))

    else:
        colwidths = [150, 60, 60, 60, 60, 60]
    tbl_summary = Table(
        data, colwidths, rowHeights=12 * mm, hAlign="LEFT", repeatRows=1
    )  #
    tbl_summary.setStyle(style_dict["feature_metrics_tblstyle"])
    return tbl_summary


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


def DrawLogo(c: canvas):
    image_path = logo_image_path
    img = Image(image_path)
    img.drawWidth = 45 * (img.imageWidth / img.imageHeight)
    img.drawHeight = 45

    c.drawImage(image_path, 30, A4[1] - 45, img.drawWidth, img.drawHeight, mask="auto")
    c.line(10, A4[1] - 45, A4[0], A4[1] - 45)


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


def pie_distribution(data, figsize, title):
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(aspect="equal"))

    X = data["categories"]
    Y = data["values"]
    colors = pie_colors
    wedges, texts = ax.pie(
        Y,
        wedgeprops=dict(width=0.6),
        startangle=90.1,
        pctdistance=0.7,
        colors=colors[0 : len(X)],
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
        # ax.annotate(fill(X[i], 14), xy=(x, y), xytext=(1.15 * np.sign(x), 1.15 * y),
        #             horizontalalignment=horizontalalignment, **kw, fontsize=annotate_fontsize, wrap=True)

    # ax.pie(Y, autopct=lambda pct: '{:d}\n({:.1f}%)'.format(ceil(pct / 100 * sum(Y)), pct), shadow=False, startangle=90.1,
    #     wedgeprops={"width": 0.6}, textprops={'fontsize': pie_textprops_fontsize}, pctdistance=0.7, colors=colors[0:len(X)])
    ax.pie(
        Y,
        autopct=lambda pct: "{:d}".format(ceil(pct / 100 * sum(Y))),
        shadow=False,
        startangle=90.1,
        wedgeprops={"width": 0.6},
        textprops={"fontsize": pie_textprops_fontsize},
        pctdistance=0.7,
        colors=colors[0 : len(X)],
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
    ax.set_title(
        title,
        loc="left",
        fontdict={"size": 11, "family": ["Calibri"], "weight": "bold"},
        y=1.15,
    )

    imgdata = io.BytesIO()

    fig.savefig(imgdata, format="PDF")

    return imgdata


def label_distributions(data):
    imgdata = pie_distribution(data=data, figsize=(5, 3.8), title=None)
    pi_item = PdfImage(imgdata)
    return Table([[pi_item]])  # colWidths=[200]) #hAlign='CENTER'


def pie_metrics(data, color):
    fig, ax = plt.subplots(figsize=(1.05, 1.05), subplot_kw={"projection": "polar"})
    startangle = 90
    x = (data * pi * 2) / 100
    left = (startangle * pi * 2) / 360  # this is to control where the bar starts
    plt.xticks([])
    plt.yticks([])
    ax.spines.clear()
    ax.barh(1, pi * 2, left=left, height=1.5, color="#F5F5F5")
    ax.barh(1, x, left=left, height=1.5, color=color)
    plt.ylim(-3, 3)
    plt.text(0, -3, str(data) + "%", ha="center", va="center", fontsize=10)

    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="PDF")
    return imgdata


def draw_accuracy_metrics(data, color):
    widths_list = [70, 80, 45, 80, 45, 80, 65]
    metrics_name = Paragraph(
        f"""<b>{str(data["metrics"])}</b>""", style=style_dict["metrics_name"]
    )
    Table_data = [metrics_name]

    imgdata = pie_metrics(data=data["value_list"][0], color=color)
    pi_image = PdfImage(imgdata)
    Table_data.append(pi_image)

    tbl_summary = Table([Table_data], widths_list, hAlign="LEFT")
    tbl_summary.setStyle(style_dict["metrics_tblstyle"])
    return tbl_summary


def draw_metrics(data, color):
    widths_list = [70, 80, 45, 80, 45, 80, 65]
    metrics_name = Paragraph(
        f"""<b>{str(data["metrics"])}</b>""", style=style_dict["metrics_name"]
    )
    Table_data = [metrics_name]
    metrics_method = ["Micro", "Macro", "Weighted"]
    metrics_method_list = [
        Paragraph(metrics_method[i], style=style_dict["metrics_method"])
        for i in range(len(metrics_method))
    ]
    for item in range(len(data["value_list"])):
        imgdata = pie_metrics(data=data["value_list"][item], color=color)
        pi_image = PdfImage(imgdata)
        Table_data.append(pi_image)
        Table_data.append(metrics_method_list[item])
    tbl_summary = Table([Table_data], widths_list, hAlign="LEFT")  #
    tbl_summary.setStyle(style_dict["metrics_tblstyle"])
    return tbl_summary


def heatmap(
    data, row_labels, col_labels, ax=None, cbar_kw=None, cbarlabel="", **kwargs
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
    im = ax.imshow(data, aspect="auto", **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(
        im, ax=ax, fraction=0.023, orientation="horizontal", **cbar_kw
    )  # ticks=[-1, 0, 1])
    # cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    # cbar.ax.set_ylabel(cbarlabel, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    # plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
    #          rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(
    im,
    data=None,
    valfmt="{x:.2f}",
    textcolors=("black", "white"),
    threshold=None,
    **textkw,
):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.0

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center", verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


def draw_confusion_matrix_heatmap(elements, basic_metrics_data):
    volumn_labels = basic_metrics_data["labels"]
    row_lables = basic_metrics_data["labels"]
    harvest = np.array(basic_metrics_data["matrix"])
    fig, ax = plt.subplots(dpi=800)

    im, cbar = heatmap(harvest, volumn_labels, row_lables, ax=ax, cmap="OrRd")
    # texts = annotate_heatmap(im, valfmt="{x:d}")

    fig.tight_layout()

    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="png")
    imgdata.seek(0)
    image = ImageReader(imgdata)

    img = PdfImage2(image, width=200, height=150)

    tbl_summary = Table([[img]], [200], hAlign="CENTER")

    elements.append(tbl_summary)

    return elements


# for robustness report
# draw basic info table for robustness table
def Robustness_Basic_Info_Table(data):
    colwidths = [150, 300]
    tblstyle_list = style_dict["tblstyle_list"]
    bold_list = ["Parameter", "Pixel Level Attacks", "Semantic Level Attacks"]
    for item in range(len(data)):
        if data[item][0] in bold_list:
            style_tuple = ("ALIGN", (0, item), (0, item), "LEFT")
            tblstyle_list.append(style_tuple)
            data[item][0] = Paragraph(
                f"""  <b>{str(data[item][0])}</b>""",
                style=style_dict["robustness_table_normal"],
            )
            data[item][1] = Paragraph(
                f"""  <b>{str(data[item][1])}</b>""",
                style=style_dict["robustness_table_center"],
            )

        else:
            data[item][0] = Paragraph(
                f"""{str(data[item][0])}""", style=style_dict["robustness_table_center"]
            )
            if len(data[item][1]) > 115:
                data[item][1] = Paragraph(
                    f"""{str(data[item][1])}""",
                    style=ParagraphStyle(
                        name="robustness_table_normal_samll",
                        fontName="Calibri",
                        parent=styles["Normal"],
                        fontSize=9,
                        leading=10,
                    ),
                )

            elif len(data[item][1]) > 62:
                data[item][1] = Paragraph(
                    f"""{str(data[item][1])}""",
                    style=ParagraphStyle(
                        name="robustness_table_normal_middle",
                        fontName="Calibri",
                        parent=styles["Normal"],
                        fontSize=12,
                        leading=12,
                    ),
                )
            else:
                data[item][1] = Paragraph(
                    f"""{str(data[item][1])}""",
                    style=style_dict["robustness_table_center"],
                )

    tbl_summary = Table(
        data, colwidths, rowHeights=11 * mm, hAlign="CENTER", repeatRows=1
    )
    tbl_summary.setStyle(TableStyle(tblstyle_list))
    return tbl_summary


# draw the final attack table for robustness
def robustness_attack_table(elements, data):
    colwidths = [75, 75, 55, 35, 35, 35, 40, 40, 40, 70]
    tblstyle_list = style_dict["attack_tblstyle_new_list"]

    dir_path = f"* PATH of Attack Samples: {os.path.dirname(data[1][0])}."
    dir_path2 = f"** PATH of Seeds: {os.path.dirname(data[1][1])}."
    for item in range(1, len(data)):
        data[item][0] = os.path.basename(data[item][0])
        data[item][1] = os.path.basename(data[item][1])
    data0 = data[0]
    data[0] = [
        Paragraph(f"<b>{data0[0]} <sup>*</sup></b>"),
        Paragraph(f"<b>{data0[1]} <sup>**</sup></b>"),
        Paragraph(f"<b>{data0[2]}</b>"),
        Paragraph(f"<b>{data0[3]}</b>"),
        Paragraph(f"<b>{data0[4]}</b>"),
        Paragraph("<b><i>L<sub>0</sub></i></b>"),
        Paragraph("<b><i>L<sub>1</sub></i></b>"),
        Paragraph("<b><i>L<sub>2</sub></i></b>"),
        Paragraph("<b><i>L<sub>inf</sub></i></b>"),
        Paragraph(f"<b>{data0[9]}</b>"),
    ]

    tbl_summary = Table(
        data, colwidths, rowHeights=8 * mm, hAlign="CENTER", repeatRows=1
    )
    tbl_summary.setStyle(TableStyle(tblstyle_list))

    elements.append(
        Paragraph(
            dir_path,
            style=ParagraphStyle(
                name="dir_normal",
                fontName="Calibri",
                parent=styles["Normal"],
                fontSize=7,
                leading=7,
            ),
        )
    )
    elements.append(
        Paragraph(
            dir_path2,
            style=ParagraphStyle(
                name="dir_normal",
                fontName="Calibri",
                parent=styles["Normal"],
                fontSize=7,
                leading=7,
            ),
        )
    )
    elements.append(Spacer(1, 2 * mm))
    elements.append(tbl_summary)

    return elements


def robustness_definition(data):
    tbl_summary = Table(data, rowHeights=11 * mm, hAlign="CENTER", repeatRows=1)
    return tbl_summary


# plot curve for robustness
def curve_distribution(data, xiax, distance):
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    ax_cur = ax
    ax.set_axisbelow(True)
    ax_cur.grid(ls="-", axis="y", color="#C0C0C0", alpha=0.3)
    ax_cur.spines["top"].set_visible(False)
    ax_cur.spines["right"].set_visible(False)
    legends_labels = list(data.keys())
    x_levels = [f"{distance}_{str(item+1)}" for item in range(len(xiax))]
    x_levels_num = [int((item)) if item > 1 else str(round(item, 4)) for item in xiax]

    # x_levels_text = '; '.join([
    #     f"{distance}_{str(item+1)}: {x_levels_num[item]}"
    #     for item in range(len(x_levels_num))
    # ])

    join_length = ceil(len(x_levels_num) / 2)

    x_levels_text = "\n".join(
        [
            f"The middle value between the upper and lower bounds of each bucket:",
            "; ".join(
                [
                    f"{distance}_{str(item+1)}: {x_levels_num[item]}"
                    for item in range(0, join_length)
                ]
            ),
            "; ".join(
                [
                    f"{distance}_{str(item+1)}: {x_levels_num[item]}"
                    for item in range(join_length, len(x_levels_num))
                ]
            ),
        ]
    )

    for item in range(len(legends_labels)):
        y_list = data[legends_labels[item]]
        if legends_labels[item] == "total dataset":
            ax.plot(
                x_levels,
                y_list,
                c=bar_colors[item],
                linewidth=3,
                marker="o",
                markersize=4,
                markerfacecolor="white",
                markeredgewidth=2,
                linestyle="-",
                label=legends_labels[item],
            )
        else:
            ax.plot(
                x_levels,
                y_list,
                c=bar_colors[item],
                linewidth=1,
                marker="o",
                markersize=2,
                markerfacecolor="white",
                markeredgewidth=1,
                linestyle="-",
                label=legends_labels[item],
            )

    plt.legend(
        bbox_to_anchor=(0.5, 1.15),
        loc="upper center",
        frameon=False,
        ncol=3,
        fontsize=6,
    )
    plt.xticks(fontproperties="Calibri", fontsize=5)
    plt.yticks(fontproperties="Calibri", fontsize=6)
    plt.ylim(0, 1)

    plt.figtext(0.1, 0.00, x_levels_text, wrap=True, ha="left", va="top", fontsize=5)
    # fig.subplots_adjust(bottom=0.3)
    # plt.tight_layout()
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="PDF", bbox_inches="tight")
    return imgdata


def robustness_curve(elements, data):
    imgdata_cur1 = curve_distribution(
        data["class_ASR"], data["xiax"], distance=data["distance"]
    )
    imgdata_cur2 = curve_distribution(
        data["method_ASR"], data["xiax"], distance=data["distance"]
    )
    colwidths = [275, 275]
    elements.append(
        Table([[PdfImage(imgdata_cur1), PdfImage(imgdata_cur2)]], colwidths)
    )
    elements.append(Spacer(1, 4 * mm))
    return elements


# plot barh for robustness
def robustness_barh_img(data, figsize, colors):
    plt.rcParams["font.sans-serif"] = ["Calibri"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=figsize)
    x = data["x"]
    ass = np.array(data["ass"])
    fail = np.array(data["fail"])

    ax_cur = ax
    ax.set_axisbelow(True)
    ax_cur.grid(ls="-", axis="x", color="#C0C0C0", alpha=0.3)
    ax_cur.spines["top"].set_visible(False)
    ax_cur.spines["right"].set_visible(False)

    height = 0.6
    ax_cur.barh(x, ass, height=height, color=colors[0], label="ASS")
    ax_cur.barh(x, fail, left=ass, height=height, color=colors[1], label="Fail")
    plt.legend(
        bbox_to_anchor=(0.5, -0.25),
        loc="lower center",
        borderaxespad=0,
        frameon=False,
        ncol=2,
    )
    plt.bar_label(ax.containers[0], label_type="center", labels=ass, alpha=0.5)
    plt.bar_label(ax.containers[1], label_type="center", labels=fail, alpha=0.5)

    plt.tight_layout()
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="PDF")
    return imgdata


def robustness_barh(elements, data):
    imgdata = robustness_barh_img(
        data=data, figsize=[6, 5], colors=["#FFA07A", "#87CEFA"]
    )
    elements.append(Table([[PdfImage(imgdata)]], hAlign="CENTER"))
    return elements


# plot bar for robustness about label distribution
def robustness_bar_distribution(data, figsize, colors, title):
    X = data["categories"]
    Y = data["values"]
    max_index = Y.index(max(Y))
    my_colors = [colors[1]] * len(Y)  # colors[0:len(X)]
    my_colors[max_index] = colors[0]

    fig, ax = plt.subplots(figsize=figsize)
    ax_cur = ax
    ax.set_axisbelow(True)
    ax_cur.grid(ls="-", axis="y", color="#C0C0C0", alpha=0.3)

    p = ax_cur.bar(X, Y, color=my_colors)
    ax.set_title(title, fontdict={"size": 13, "family": ["Calibri"], "weight": "bold"})
    ax_cur.spines["top"].set_visible(False)
    ax_cur.spines["right"].set_visible(False)
    ax.bar_label(p, fontsize=8)

    plt.xticks(arange(len(X)), [fill(item, 13) for item in X], wrap=True, fontsize=8)
    plt.yticks(wrap=True, fontsize=8)

    plt.ylim(0, 1)
    plt.tight_layout()

    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="PDF")
    return imgdata


def robustness_label_distributions(elements, data, titles):
    data = sorted(data.items(), key=lambda x: x[1]["ASR"], reverse=True)

    categories = (
        [sub[0] for sub in data] if len(data) <= 6 else [sub[0] for sub in data[0:5]]
    )

    asr_data = {
        "categories": categories,
        "values": [sub[1]["ASR"] for sub in data]
        if len(data) <= 6
        else [sub[1]["ASR"] for sub in data[0:5]],
    }

    imgdata = robustness_bar_distribution(
        data=asr_data, figsize=(5, 3.8), colors=bar_colors, title=titles[0]
    )

    elements.append(Table([[PdfImage(imgdata)]], hAlign="CENTER"))

    if len(data) > 6:
        samples = 0
        for sub in data[5:]:
            samples += sub[1]["attack_samples"]

        attack_samples = {
            "categories": categories + ["other"],
            "values": [sub[1]["attack_samples"] for sub in data[0:5]] + [samples],
        }
    else:
        attack_samples = {
            "categories": categories,
            "values": [sub[1]["attack_samples"] for sub in data],
        }

    imgdata_pie1 = pie_distribution(attack_samples, figsize=(3.1, 3.5), title=titles[1])

    if len(data) > 6:
        samples = 0
        for sub in data[5:]:
            samples += sub[1]["attack_success"]

        attack_success = {
            "categories": categories + ["other"],
            "values": [sub[1]["attack_success"] for sub in data[0:5]] + [samples],
        }
    else:
        attack_success = {
            "categories": categories,
            "values": [sub[1]["attack_success"] for sub in data],
        }

    imgdata_pie2 = pie_distribution(attack_success, figsize=(3.1, 3.5), title=titles[2])

    colwidths = [285, 285]
    # elements.append(Spacer(1, 15 * mm))
    elements.append(
        Table(
            [[PdfImage(imgdata_pie1), PdfImage(imgdata_pie2)]],
            colwidths,
            hAlign="CENTER",
        )
    )

    return elements


# conclusion for robustness
def robustness_conclusion(elements, data):
    tbl_summary = Table([[data]], colWidths=[500], rowHeights=60, hAlign="CENTER")
    tbl_summary.setStyle(style_dict["conclusion_tblstyle"])
    elements.append(tbl_summary)
    return elements


# create reports
# create report for basic metrics
def basic_metrics_report(filename, data):
    result_dict = eval(data[0]["result"])
    # result_keys = list(result_dict.keys())  #dict_keys(['basic_metrics', 'slices_basic_metrics', 'labels'])
    labels = result_dict["labels"]
    slices_basic_metrics = result_dict["slices_basic_metrics"]["one_odd"]
    # slices_basic_metrics_one_odd.keys:   dict_keys(['augmentation', 'Fog_intensity', 'Snowfall_intensity', 'Illuminance', 'Rain_quantity'])

    basic_metrics = result_dict["basic_metrics"]

    elements = [Paragraph("<b>Basic Metrics Testing Report</b>", style_dict["title"])]
    basic_info = [
        f"""Model: {data[0]['model_path']}""",
        f"""Dataset: {data[0]['data_path']}""",
        f"""Machineinfo:  {data[0]['machine_info']}""",
        f"""Createtime: {data[0]['create_time']}""",
    ]
    elements.append(Spacer(1, 3 * mm))
    elements.append(Paragraph("<b>Basic Information</b>", style_dict["heading1"]))
    image_path = blue_image_path
    img = Image(image_path, hAlign="LEFT")
    img.drawWidth = 10 * (img.imageWidth / img.imageHeight)
    img.drawHeight = 10
    elements.append(img)
    for item in range(len(basic_info)):
        elements.append(Paragraph(basic_info[item], style=style_dict["no_order_list"]))
    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph("<b>Test Result</b>", style_dict["heading1"]))
    elements.append(img)
    elements.append(
        Paragraph(
            "<b><i>Basic Metrics on full dataset</i></b>", style=style_dict["heading2"]
        )
    )
    samples_number = basic_metrics["samples"]
    dataset_class_no = len(labels)
    dataset_class = ",".join(labels)
    ptext = f"""There are <a color='#c00000'><b>{samples_number}</b></a> samples in full datasets, including <a color='#c00000'><b>{dataset_class_no}</b></a> categories ({dataset_class}). """
    elements.append(Paragraph(ptext, style=style_dict["normal"]))
    ptext = "The related test results are as follows:"
    elements.append(Paragraph(ptext, style=style_dict["normal"]))
    ptext = "<a color='#c00000'><b>Fig1. The distribution of each class</b></a>"
    elements.append(Paragraph(ptext, style=style_dict["normal"]))
    label_data = {
        "categories": list(basic_metrics["distribution"].keys()),
        "values": list(basic_metrics["distribution"].values()),
    }

    # label_color_list = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272']
    elements.append(label_distributions(data=label_data))

    ptext = "<a color='#c00000'><b>Fig2. Each basic metrics calculated on full dataset</b></a>"
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    elements.append(
        draw_accuracy_metrics(
            data={
                "metrics": "Accuracy",
                "value_list": [int(basic_metrics["total*accuracy"] * 100)],
            },
            color="#d5ba82",
        )
    )

    elements.append(
        draw_metrics(
            data={
                "metrics": "Precision",
                "value_list": [
                    int(basic_metrics["micro*precision"] * 100),
                    int(basic_metrics["macro*precision"] * 100),
                    int(basic_metrics["weighted*precision"] * 100),
                ],
            },
            color="#597c8b",
        )
    )
    elements.append(
        draw_metrics(
            data={
                "metrics": "Recall",
                "value_list": [
                    int(basic_metrics["micro*recall"] * 100),
                    int(basic_metrics["macro*recall"] * 100),
                    int(basic_metrics["weighted*recall"] * 100),
                ],
            },
            color="#d6bbc1",
        )
    )
    elements.append(
        draw_metrics(
            data={
                "metrics": "F1-score",
                "value_list": [
                    int(basic_metrics["micro*f1score"] * 100),
                    int(basic_metrics["macro*f1score"] * 100),
                    int(basic_metrics["weighted*f1score"] * 100),
                ],
            },
            color="#b36a6f",
        )
    )

    elements.append(Spacer(1, 0.1 * inch))
    ptext = "<a color='#c00000'><b>Fig3. Confusion matrix on full dataset</b></a>"
    elements.append(Paragraph(ptext, style=style_dict["normal"]))
    elements.append(Spacer(1, 0.1 * inch))

    basic_metrics_data = {
        "labels": result_dict["labels"],
        "matrix": basic_metrics["matrix"],
    }

    elements = draw_confusion_matrix_heatmap(elements, basic_metrics_data)

    elements.append(
        Paragraph(
            "<b><i>Basic Metrics on different data slices</i></b>",
            style=style_dict["heading2"],
        )
    )

    features = list(slices_basic_metrics.keys())

    ptext = f"""There are <a color='#c00000'><b> {len(features)} </b></a> countable feature dimensions in the full dataset."""
    elements.append(Paragraph(ptext, style=style_dict["normal"]))
    ptext = f"""The distribution of each dimension are as follows:"""
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    # label_color_list = [
    #     "#5470c6",
    #     "#91cc75",
    #     "#fac858",
    #     "#ee6666",
    #     "#73c0de",
    #     "#3ba272",
    # ]
    for item in range(len(features)):
        ptext = f"""<a color='#c00000'><b>Fig 4-{item + 1}. The distribution of {features[item]} </b></a> """
        elements.append(Paragraph(ptext, style=style_dict["normal"]))

        labels_for_feature = slices_basic_metrics[features[item]]["values"]
        feature_keys = list(slices_basic_metrics[features[item]].keys())
        label_data = {
            "categories": labels_for_feature,
            "values": [
                slices_basic_metrics[features[item]][feature_keys[i]]["samples"]
                for i in range(len(labels_for_feature))
            ],
        }

        elements.append(label_distributions(data=label_data))

    elements.append(Spacer(1, 0.1 * inch))
    ptext = f"""The basic metrics on each feature are as follows:"""
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    for item in range(len(features)):
        ptext = f"""<a color='#c00000'><b>Table 1-{item + 1}. Basic metrics on {features[item]} </b></a> """
        elements.append(Paragraph(ptext, style=style_dict["normal"]))
        elements.append(Spacer(1, 0.05 * inch))
        slices_data = slices_basic_metrics[features[item]]
        Basic_table = metrics_table(slice_data=slices_data)
        elements.append(Basic_Metrics_Table(data=Basic_table))
        elements.append(Spacer(1, 0.2 * inch))

    doc = SimpleDocTemplate(filename)
    doc.build(elements, canvasmaker=PageNumCanvas)


# create report for robustness
def robustness_report(filename, data):
    image_path = blue_image_path
    img = Image(image_path, hAlign="LEFT")
    img.drawWidth = 10 * (img.imageWidth / img.imageHeight)
    img.drawHeight = 10

    elements = [
        Paragraph("<b>Robustness Testing Report</b>", style_dict["title"]),
        Spacer(1, 4 * mm),
        Paragraph("<b>Basic Information</b>", style_dict["heading1"]),
        img,
        Spacer(1, 3 * mm),
    ]

    raw_hyperparameter = eval(data[0]["raw_hyperparameter"])
    result = eval(data[0]["result"])
    result_path = data[0]["result_path"]

    basic_info = [
        ["Parameter", "Value"],
        ["Model", data[0]["model_path"]],
        ["Model Framework", raw_hyperparameter["model_framework"]],
        ["Domain", raw_hyperparameter["domain"]],
        ["Task Type", raw_hyperparameter["task_type"]],
        ["DataSet", data[0]["data_path"]],
        ["Model Type", raw_hyperparameter["model_type"]],
        ["Mutation Guidance", raw_hyperparameter["mutation_guidance"]],
        [
            "Related Param",
            f""" p_min = {raw_hyperparameter['p_min']}; k_time = {raw_hyperparameter['k_time']}; r = {raw_hyperparameter['r']}; 
        try_num = {raw_hyperparameter['try_num']}; alpha ={raw_hyperparameter['alpha']}; beta = {raw_hyperparameter['beta']}; 
        max_iter = {raw_hyperparameter['max_iter']}; batch_size = {raw_hyperparameter['batch_size']}
""",
        ],
        ["Pixel Level Attacks", ""],
    ]
    basic_info.extend(
        [
            [
                sub_method["method"],
                ";".join(
                    [
                        f"{sub_param['name']}={[eval(sub) for sub in sub_param['value'].split(',')] if ',' in sub_param['value'] else sub_param['value']}"
                        for sub_param in sub_method["parameters"]
                    ]
                ),
            ]
            for sub_method in raw_hyperparameter["pixel_level"]
        ]
    )
    # ['Method1', f'{sub['']}={value}' for sub in raw_hyperparameter['pixel_level']],
    # ['Method2', f""" a= 1; b = 2; c = 3"""],
    basic_info.append(["Semantic Level Attacks", ""])
    basic_info.extend(
        [
            [
                sub_method["method"],
                ";".join(
                    [
                        f"{sub_param['name']}={[eval(sub) for sub in sub_param['value'].split(',')] if ',' in sub_param['value'] else sub_param['value']}"
                        for sub_param in sub_method["parameters"]
                    ]
                ),
            ]
            for sub_method in raw_hyperparameter["semantic_level"]
        ]
    )
    # ['Method1', f""" a= 1; b = 2; c = 3"""],
    # ['Method2', f""" a= 1; b = 2; c = 3"""],

    elements.append(Robustness_Basic_Info_Table(basic_info))

    Part2_list = [
        Spacer(1, 3 * mm),
        Paragraph("<b>Explanation of relevant definitions</b>", style_dict["heading1"]),
        img,
        Spacer(1, 3 * mm),
    ]
    elements += Part2_list

    ptext = f""" For adversarial attacks in Computer Vision field, we have some metrics to show, including 
    <a color='#c00000'><b>  Attack Success Rate (ASR) </b></a> , the attack distance(
    <a color='#c00000'><b>  <i>L<sub>0</sub></i> </b></a>, 
    <a color='#c00000'><b>  <i>L<sub>1</sub></i> </b></a>, 
    <a color='#c00000'><b>  <i>L<sub>2</sub></i> </b></a>, 
    <a color='#c00000'><b>  <i>L<sub>inf</sub></i> </b></a>, 
    and 
    <a color='#c00000'><b> Structural Similarity(SSIM) </b></a>. 
    """

    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    definisions = [
        Paragraph(
            f""" <a color='#c00000'><b> ASR (Attack Success Rate) : </b></a> The proportion of adversarial examples 
            that prevent the model from outputting correct results. It is used to evaluate the effectiveness of the attack 
            methods.""",
            style=style_dict["no_order_list_robustness"],
        ),
        Paragraph(
            f"""<a color='#c00000'><b> Adversarial Sample / Example : </b></a>  An input sample
        generated by intentionally adding subtle perturbations to the data, which can cause a neural network model to
        give an incorrect prediction result.""",
            style=style_dict["no_order_list_robustness"],
        ),
        Paragraph(
            f"""<a color='#c00000'><b> <i>L<sub>0</sub></i> : </b></a>  It is mainly used to measure the number 
        of non-zero elements in a vector. In adversarial examples, the <i>L<sub>0</sub></i> norm measures the number of 
        mismatched elements between the adversarial sample and the original data. For computer vision field, it usually 
        refers to the number of pixels modified by the adversarial example relative to the original image. It focuses on 
        the number of pixels that have mutated, not the degree of mutation..""",
            style=style_dict["no_order_list_robustness"],
        ),
        Paragraph(
            f"""<a color='#c00000'><b> <i>L<sub>1</sub></i> : </b></a> The <i>L<sub>1</sub></i> norm has many names, such as Manhattan Distance , 
        minimum absolute error, etc. It can be used to measure the difference between two vectors, representing the sum 
        of absolute values of non-zero elements in the vector. In adversarial examples, it refers to the sum of the 
        absolute values of the differences between the pixels of the adversarial example and the original image.""",
            style=style_dict["no_order_list_robustness"],
        ),
        Paragraph(
            f"""<a color='#c00000'><b> <i>L<sub>2</sub></i> : </b></a> The <i>L<sub>2</sub></i> norm measures 
        the standard Euclidean distance between two vectors. In adversarial examples, it usually refers to the 
        square root of the sum of squared changes in the modified pixels of the adversarial example relative to 
        the original image.""",
            style=style_dict["no_order_list_robustness"],
        ),
        Paragraph(
            f"""<a color='#c00000'><b> <i>L<sub>inf</sub></i> : </b></a> The infinite norm is mainly used to 
        measure the maximum value of vector elements. In adversarial examples, it usually refers to the maximum 
        absolute value of the change in the modified pixels relative to the original image in the adversarial example.""",
            style=style_dict["no_order_list_robustness"],
        ),
        Paragraph(
            f"""<a color='#c00000'><b> Structural Similarity (SSIM) : </b></a> It is a fully referenced image quality 
        evaluation indicator that measures the similarity between two images from three aspects: brightness, contrast, 
        and structure. The larger the value, the better, with a maximum of 1. When the two images are identical, 
        the SSIM index is equal to 1.""",
            style=style_dict["no_order_list_robustness"],
        ),
    ]

    for item in range(len(definisions)):
        elements.append(definisions[item])

    # definisions = [
    #     [Paragraph(f"""【ASR(Attack Success Rate) 】 xxxxxxxxxxxxx, e.g. xxxxx""", style=styles["Normal"])],
    #     [Paragraph(f"""【AS(Attack Sample) 】 xxxxxxxxxxxxx, e.g. xxxxx""", style=styles["Normal"])],
    #     [Paragraph("<i>【L</i><sub>0</sub> distance 】xxxxxxxxxxxxx, e.g. xxxxx", style=styles["Normal"])],
    #     [Paragraph("<i>【L</i><sub>1</sub> distance 】xxxxxxxxxxxxx, e.g. xxxxx", style=styles["Normal"])],
    #     [Paragraph("<i>【L</i><sub>2</sub> distance 】xxxxxxxxxxxxx, e.g. xxxxx", style=styles["Normal"])],
    #     [Paragraph("<i>【L</i><sub>inf</sub> distance 】xxxxxxxxxxxxx, e.g. xxxxx", style=styles["Normal"])],
    #     [Paragraph("【Structural Dissimilarity 】xxxxxxxxxxxxx, e.g. xxxxx", style=styles["Normal"])]
    # ]

    # elements.append(robustness_definition(definisions))

    Part3_list = [
        Spacer(1, 3 * mm),
        Paragraph("<b>Test Result</b>", style_dict["heading1"]),
        img,
        Spacer(1, 3 * mm),
    ]
    elements += Part3_list

    samples_number = result["total_samples"]
    labels = result["labels"]
    dataset_class_no = len(labels)
    dataset_class = ", ".join(labels)

    ptext = f"""There are <a color='#c00000'><b>{samples_number}</b></a> samples in full datasets, including <a color='#c00000'><b>{dataset_class_no}</b></a> classes ({dataset_class}). The related test results are as follows:"""
    elements.append(Paragraph(ptext, style=style_dict["normal"]))
    ptext = "<a color='#c00000'><b>Fig1. The distribution of each class</b></a>"
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    # label_data = {
    #     "categories": labels,
    #     "values": list(range(1, 7))
    # }
    label_data = {
        "categories": list(result["distribution"].keys()),
        "values": list(result["distribution"].values()),
    }
    elements.append(label_distributions(data=label_data))

    ptext = "<a color='#c00000'><b>Fig2. Comparison between different sample categories</b></a>"
    # elements.append(Spacer(1, 3 * mm))
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    if len(labels) >= 5:
        ptext = f"""The chart only includes the <a color='#c00000'><b>Top5</b></a> categories, 
        while the remaining categories are included in "others". 
        If you need the details, you can view them on the page."""
        elements.append(Paragraph(ptext, style=style_dict["normal"]))
    # label_data = {
    #     "categories": ["CL1", "CL2", "CL3", "CL4", "CL5"],
    #     "values": [0.65, 0.82, 0.75, 0.59, 0.56]
    # }

    titles = [
        "The Attacks Success Rate in different categories",
        "# Attack samples",
        "# Attack Success samples",
    ]

    elements = robustness_label_distributions(
        elements=elements, data=result["label_slices"], titles=titles
    )

    chart_show = f""" The chart shows that ..."""
    ptext = Paragraph(
        f"<b>Conclusion:</b> {chart_show}", style_dict["conclusion_normal"]
    )

    elements = robustness_conclusion(elements=elements, data=ptext)

    ptext = "<a color='#c00000'><b>Fig3. Comparison between different Attack Methods</b></a>"
    elements.append(Spacer(1, 5 * mm))
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    # methods = ['method_1', 'method_2', 'method_3', 'method_4', 'method_5', 'method_6']
    methods = list(result["method_slices"].keys())

    # method_chosen = ''result['method_slices']
    method_chosen_list = ", ".join(methods)
    # method_selected = methods[0:4]
    method_selected_list = ", ".join(methods)
    ptext = f""" <b>Comments</b>: You have chosen these attack methods: {method_chosen_list}, etc.
    But the method was randomly selected, and the attack methods used in this test include {method_selected_list},etc.
    """
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    titles = [
        "The Attacks Success Rate in different methods",
        "# Attack samples",
        "# Attack Success samples",
    ]

    elements = robustness_label_distributions(
        elements=elements, data=result["method_slices"], titles=titles
    )

    chart_show = f""" The chart shows that ..."""
    ptext = Paragraph(
        f"<b>Conclusion:</b> {chart_show}", style_dict["conclusion_normal"]
    )

    elements = robustness_conclusion(elements=elements, data=ptext)

    ptext = "<a color='#c00000'><b>Fig4. Comparison of attack methods and categories</b></a>"
    elements.append(Spacer(1, 5 * mm))
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    ptext = f""" The chart only includes the <a color='#c00000'><b>TOP 10</b></a> combinations of categories & adverarial methods based on the number of successful attack samples in descending order. If you need to view more categories and methods, you can view them on the page.
    """
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    ptext = f""" <a color='#c00000'><b>ASS</b></a> shows the number of successful attack samples. <a color='#c00000'><b>Fail</b></a> shows the number of samples that failed attack.
    """
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    label_method_slices = sorted(
        result["label_method_slices"].items(),
        key=lambda x: (x[1]["attack_success"], x[1]["attack_failed"]),
        reverse=False,
    )

    # data = {
    #     'x': ['CL1_M1', 'CL1_M2', 'CL1_M3', 'CL2_M1', 'CL2_M2', 'CL2_M3', 'CL3_M1', 'CL3_M2', 'CL3_M3'],
    #     'ass': [120, 110, 150, 120, 110, 150, 120, 110, 150],
    #     'fail': [80, 95, 64, 80, 95, 64, 80, 95, 64]
    # }
    data = {}

    for key, value in label_method_slices[-10:]:
        data.setdefault("x", []).append(key.replace("*", " & "))
        data.setdefault("ass", []).append(value["attack_success"])
        data.setdefault("fail", []).append(value["attack_failed"])

    elements = robustness_barh(elements=elements, data=data)

    # ass_new = []
    # fail_new = []
    # index_list = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    # for item in range(len(index_list)):
    #     ass_new.append(data['ass'][index_list[item]])
    #     fail_new.append(data['fail'][index_list[item]])
    #
    # data = {
    #     'x': ['M1_CL1', 'M1_CL2', 'M1_CL3', 'M2_CL1', 'M2_CL2', 'M2_CL3', 'M3_CL1', 'M3_CL2', 'M3_CL3'],
    #     'ass': ass_new,
    #     'fail': fail_new
    # }
    # elements = robustness_barh(elements=elements, data=data)
    chart_show = f""" The chart shows that ..."""
    ptext = Paragraph(
        f"<b>Conclusion:</b> {chart_show}", style_dict["conclusion_normal"]
    )

    elements = robustness_conclusion(elements=elements, data=ptext)

    ptext = "<a color='#c00000'><b>Fig5. The comparison of ASR between different category/method and distance </b></a>"
    elements.append(Spacer(1, 5 * mm))
    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    ptext = f""" The following will calculate the L0 (L1, L2, Linf, Structural Similarity) distance between all mutated samples and the original sample using the distance formula of L0 (L1, L2, Linf, Structural Similarity), 
    and use all L0 (L1, L2, Linf, Structural Similarity) distance values as 10 buckets to measure the level of differentiation between samples. 
    The ratio of successful adversarial samples to the total number of samples counted in each bucket will be used as the attack success rate (ASR) within that bucket. 
    According to different categories and methods, the above statistical methods can be used, and the following Line chart shows the change trend of ASR with the change of sample distance level.    
    """

    elements.append(Paragraph(ptext, style=style_dict["normal"]))

    if len(labels) > 5 or len(methods) > 5:
        ptext = f""" 
        The chart only includes the <a color='#c00000'><b>Top5</b></a> categories and methods. If you need to view more categories and methods, please refer to the web page.
        """
        elements.append(Paragraph(ptext, style=style_dict["normal"]))

    class_data = sorted(
        result["label_slices"].items(), key=lambda x: x[1]["ASR"], reverse=True
    )

    method_data = sorted(
        result["method_slices"].items(), key=lambda x: x[1]["ASR"], reverse=True
    )

    # for distance, distance_name in {'l0': 'L0', 'l1': 'L1', 'l2': 'L2', 'linf': 'Linf', 'ssim': 'Structural Dissimilarity'}.items():
    for distance, distance_name in {
        "l0": "L0",
        "l1": "L1",
        "l2": "L2",
        "linf": "Linf",
        "ssim": "ssim",
    }.items():
        ASR_data = {
            "distance": distance_name,
            "xiax": list(result["total_distance"]["distance_detail"][distance].keys()),
            "class_ASR": {
                "total dataset": list(
                    result["total_distance"]["distance_detail"][distance].values()
                )
            }
            # "class_ASR": {
            #     'total dataset': [0.02, 0.1, 0.13, 0.22, 0.3, 0.42, 0.58],
            #     'Class1': [0.05, 0.18, 0.22, 0.35, 0.42, 0.57, 0.79],
            #     'Class2': [0.1, 0.19, 0.22, 0.4, 0.48, 0.52, 0.7],
            #     'Class3': [0.18, 0.2, 0.25, 0.28, 0.38, 0.42, 0.72],
            #     'Class4': [0.32, 0.33, 0.43, 0.52, 0.6, 0.72, 0.81],
            #     'Class5': [0.1, 0.19, 0.22, 0.40, 0.42, 0.48, 0.62],
            # },
            #
            # "method_ASR": {
            #     'Method1': [0.05, 0.18, 0.22, 0.35, 0.42, 0.57, 0.79],
            #     'Method2': [0.1, 0.19, 0.22, 0.4, 0.48, 0.52, 0.7],
            #     'Method3': [0.18, 0.2, 0.25, 0.28, 0.38, 0.42, 0.72],
            #     'Method4': [0.32, 0.33, 0.43, 0.52, 0.6, 0.72, 0.81],
            #     'Method5': [0.1, 0.19, 0.22, 0.40, 0.42, 0.48, 0.62],
            # }
        }

        for sub_class in class_data[:5]:
            ASR_data.setdefault("class_ASR", {}).setdefault(
                sub_class[0], list(sub_class[1]["distance_detail"][distance].values())
            )
        for sub_method in method_data[:5]:
            ASR_data.setdefault("method_ASR", {}).setdefault(
                sub_method[0], list(sub_method[1]["distance_detail"][distance].values())
            )

        elements = robustness_curve(elements=elements, data=ASR_data)

        chart_show = f""" As <b>{distance_name}</b> distance increase, ..."""
        ptext = Paragraph(f" {chart_show}", style_dict["conclusion_normal"])

        elements = robustness_conclusion(elements=elements, data=ptext)

    elements.append(Spacer(1, 5 * mm))
    elements.append(
        Paragraph("<b>Adversarial Samples Information</b>", style_dict["heading1"])
    )
    elements.append(img)
    elements.append(Spacer(1, 3 * mm))

    ptext = f"""There are <a color='#c00000'><b>{result['total_attack_samples']}</b></a> adversarial samples generated during the test, you can check some of the detail below
(Only 50 pieces of information are provided here. If you want to browse all the adversarial sample information, please view them on the page)."""

    elements.append(Paragraph(ptext, style=style_dict["normal"]))
    elements.append(Spacer(1, 3 * mm))

    # attack_info = [
    #     ['AS', 'Seed', 'Methods', 'True label', 'Pred label', 'L0', 'L1', 'L2', 'Linf', 'Structural Dissimilarity'],
    #     ['project/abc/***/dataset/img1.jpg', 'project/abc/***/seeds/seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    #     ['img1.jpg', 'seed1.jpg', 'I-FGSM', 'Cat', 'Dog', 0.35, 0.24, 0.83, 0.81, 0.32],
    # ]

    unzip_path = result_path.replace(".zip", "")

    with zipfile.ZipFile(result_path) as file:
        file.extractall(unzip_path)

    for root_path, dir, files in os.walk(unzip_path):
        if dir:
            with open(
                os.path.join(root_path, dir[0], "fail_test_info.txt"),
                "r",
                encoding="utf-8",
            ) as f:
                all_records = f.readlines()

    attack_first_line = [
        "saved_path",
        "from_seed_path",
        "mutated_method",
        "label",
        "pred_label",
        "l0",
        "l1",
        "l2",
        "linf",
        "ssim",
    ]

    attack_info_raw = [sub.split(":")[0] for sub in all_records[0].strip().split(",")]
    index_list = [
        i for e in attack_first_line for i, y in enumerate(attack_info_raw) if e == y
    ]

    attack_info = [
        [
            "AS",
            "Seed",
            "Methods",
            "True label",
            "Pred label",
            "L0",
            "L1",
            "L2",
            "Linf",
            "Structural Similarity",
        ]
    ]

    # attack_info.extend([[sub.split(":")[1].split('/')[-1] if '/' in sub.split(':')[1] else sub.split(":")[1]
    #                     for sub in line.strip().split(',')] for line in all_records])

    # attack_info.extend([[[sub.split(":")[1] if '/' in sub.split(':')[1] else sub.split(":")[1]
    #                     for sub in line.strip().split(',')][index] for index in index_list] for line in all_records])

    attack_info.extend(
        [
            [
                int(float(e))
                if i in list(range(5, 9))
                else round(float(e), 4)
                if i == 9
                else e
                for i, e in enumerate(
                    [
                        [
                            sub.split(":")[1]
                            if "/" in sub.split(":")[1]
                            else sub.split(":")[1]
                            for sub in line.strip().split(",")
                        ][index]
                        for index in index_list
                    ]
                )
            ]
            for line in all_records
        ]
    )

    # for line in all_records:
    #     sub_info = []
    #     for sub in line.strip().split(','):
    #         if '/' in sub.split(':')[1]:
    #             sub_info.append(sub.split(":")[1].split('/')[-1])
    #         else:
    #             sub_info.append(sub.split(":")[1])
    #     sub_info_new = []
    #     for index in index_list:
    #         sub_info_new.append(sub_info[index])

    #     for item in range(len(sub_info_new)):
    #         if item == 9:
    #             sub_info_new[item] = round(float(sub_info_new[item]), 4)
    #         elif item in list(range(5, 9)):
    #             sub_info_new[item] = int(float(sub_info_new[item]))
    #     attack_info.extend(sub_info_new)

    shutil.rmtree(unzip_path)

    elements = robustness_attack_table(elements, attack_info[:50])

    doc = SimpleDocTemplate(filename)
    doc.build(elements, canvasmaker=PageNumCanvas)
