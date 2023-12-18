# -*- coding: utf-8 -*-

"""
@author: 李强
@contact: QQ:1206709430
@Created on: 2021/6/8 003 0:30
@Remark: 操作日志管理
"""

from dvadmin.system.models import OperationLog
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class OperationLogSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = OperationLog
        fields = "__all__"
        read_only_fields = ["id"]


class OperationLogCreateUpdateSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = OperationLog
        fields = "__all__"


class OperationLogViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = OperationLog.objects.order_by("-create_datetime")
    serializer_class = OperationLogSerializer
    # permission_classes = []
