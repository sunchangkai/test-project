# -*- coding: utf-8 -*-
# @Time    : 2023/1/13 上午2:49
# @Author  : liuliping
# @File    : urls.py
# @description:


from rest_framework.routers import SimpleRouter
from django.urls import path

from prosafeAI.views.basic_info.prosafeAI_project import ProsafeAIProjectViewSet
from prosafeAI.views.basic_info.prosafeAI_field import ProsafeAIFieldViewSet
from prosafeAI.views.basic_info.prosafeAI_odd import ProsafeAIOddViewSet
from prosafeAI.views.basic_info.prosafeAI_table import ProsafeAITableViewSet
from prosafeAI.views.basic_info.prosafeAI_usercase import ProsafeAIUsercaseViewSet
from .views.data_management.table_details import TableDetailsView
from .views.data_management.get_tables import TablesView
from .views.data_management.table_version_info import VersionInfoView
from .views.data_management.table_field_info import FieldInfoView
from .views.data_management.table_object_tag_details import TableObjectTagDetailsView
from .views.data_management.import_data import ImportDataViewSet
from .views.data_display.data_statistics import DataStatisticsViewSet
from .views.data_verification.get_task_table import TaskTableView
from .views.data_verification.get_result_table import ResultTableView
from .views.data_verification.get_requirements_list import RequirementsTableView
from .views.data_verification.get_sub_requirements import SubRequirementsTableView
from .views.data_verification.import_task import ImportTaskViewSet
from .views.data_verification.run_verification import RunVerificationViewSet
from .views.data_verification.export_report import ExportReportView
from .views.modelV_test.modelV_sdk_view import ModelVSDKViewSet
from .views.modelV_test.modelV_crud import ModelVCRUDViewSet

router = SimpleRouter()

router.register(r"prosafeai_project", ProsafeAIProjectViewSet)
router.register(r"prosafeai_usercase", ProsafeAIUsercaseViewSet)
router.register(r"prosafeai_odd", ProsafeAIOddViewSet)
router.register(r"prosafeai_table", ProsafeAITableViewSet)
router.register(r"prosafeai_field", ProsafeAIFieldViewSet)
router.register(r"data_management", ImportDataViewSet, basename="import_data")
router.register(r"data_display", DataStatisticsViewSet, basename="data_display")
router.register(r"data_verification", ImportTaskViewSet, basename="import_task")
router.register(
    r"data_verification", RunVerificationViewSet, basename="run_verification"
)
router.register(r"modelV_sdk", ModelVSDKViewSet, basename="modelV_sdk")
router.register(r"modelV_crud", ModelVCRUDViewSet, basename="modelV_crud")

urlpatterns = [
    path("prosafeai_tables/", TablesView.as_view()),
    path("table_details/", TableDetailsView.as_view()),
    path("version_info/", VersionInfoView.as_view()),
    path("table_field_info/", FieldInfoView.as_view()),
    path("object_tag_details/", TableObjectTagDetailsView.as_view()),
    path("task_list/", TaskTableView.as_view()),
    path("result_list/", ResultTableView.as_view()),
    path("requirements_list/", RequirementsTableView.as_view()),
    path("sub_requirements/", SubRequirementsTableView.as_view()),
    path("export_report/", ExportReportView.as_view()),
]
urlpatterns += router.urls
