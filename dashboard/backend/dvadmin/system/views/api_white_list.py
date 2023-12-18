# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2022/1/1 001 9:34
@Remark:
"""
from dvadmin.system.models import ApiWhiteList
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ApiWhiteListSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = ApiWhiteList
        fields = "__all__"
        read_only_fields = ["id"]


class ApiWhiteListInitSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = ApiWhiteList
        fields = ["url", "method", "enable_datasource", "creator", "dept_belong_id"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True},
        }


class ApiWhiteListViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = ApiWhiteList.objects.all()
    serializer_class = ApiWhiteListSerializer
    # permission_classes = []
