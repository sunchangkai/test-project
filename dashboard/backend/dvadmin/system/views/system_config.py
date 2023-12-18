# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2022/1/21 003 0:30
@Remark: 系统配置
"""
import django_filters
from django.db.models import Q
from django_filters.rest_framework import BooleanFilter
from rest_framework import serializers
from rest_framework.views import APIView

from application import dispatch
from dvadmin.system.models import SystemConfig
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from dvadmin.utils.models import get_all_models_objects
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomValidationError
from dvadmin.utils.viewset import CustomModelViewSet


class SystemConfigCreateSerializer(CustomModelSerializer):
    """ """

    form_item_type_label = serializers.CharField(
        source="get_form_item_type_display", read_only=True
    )

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_key(self, value):
        """
        Verify whether duplicate keys are allowed

        When the parent is empty, it is not allowed to duplicate,
        otherwise it is allowed
        """
        instance = SystemConfig.objects.filter(key=value, parent__isnull=True).exists()
        if instance:
            raise CustomValidationError("already existed")
        return value


class SystemConfigInitSerializer(CustomModelSerializer):
    """ """

    children = serializers.SerializerMethodField()

    def get_children(self, obj: SystemConfig):
        data = []
        instance = SystemConfig.objects.filter(parent_id=obj.id)
        if instance:
            serializer = SystemConfigInitSerializer(instance=instance, many=True)
            data = serializer.data
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        children = self.initial_data.get("children")
        #
        if children:
            for data in children:
                data["parent"] = instance.id
                filter_data = {"key": data["key"], "parent": data["parent"]}
                instance_obj = SystemConfig.objects.filter(**filter_data).first()
                if instance_obj and not self.initial_data.get("reset"):
                    continue
                serializer = SystemConfigInitSerializer(
                    instance_obj, data=data, request=self.request
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return instance

    class Meta:
        model = SystemConfig
        fields = [
            "parent",
            "title",
            "key",
            "value",
            "sort",
            "status",
            "data_options",
            "form_item_type",
            "rule",
            "placeholder",
            "setting",
            "creator",
            "dept_belong_id",
            "children",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True},
        }


class SystemConfigSerializer(CustomModelSerializer):
    """ """

    form_item_type_label = serializers.CharField(
        source="get_form_item_type_display", read_only=True
    )

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]


class SystemConfigChinldernSerializer(CustomModelSerializer):
    """ """

    chinldern = serializers.SerializerMethodField()
    form_item_type_label = serializers.CharField(
        source="get_form_item_type_display", read_only=True
    )

    def get_chinldern(self, instance):
        queryset = SystemConfig.objects.filter(parent=instance)
        serializer = SystemConfigSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]


class SystemConfigListSerializer(CustomModelSerializer):
    """ """

    def update(self, instance, validated_data):
        instance_mapping = {obj.id: obj for obj in instance}
        data_mapping = {item["id"]: item for item in validated_data}
        for obj_id, data in data_mapping.items():
            instance_obj = instance_mapping.get(obj_id, None)
            if instance_obj is None:
                return SystemConfig.objects.create(**data)
            else:
                return instance_obj.objects.update(**data)

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]


class SystemConfigSaveSerializer(serializers.Serializer):
    class Meta:
        read_only_fields = ["id"]
        list_serializer_class = SystemConfigListSerializer


class SystemConfigFilter(django_filters.rest_framework.FilterSet):
    """ """

    parent__isnull = BooleanFilter(field_name="parent", lookup_expr="isnull")

    class Meta:
        model = SystemConfig
        fields = ["id", "parent", "status", "parent__isnull"]


class SystemConfigViewSet(CustomModelViewSet):
    """ """

    queryset = SystemConfig.objects.order_by("sort", "create_datetime")
    serializer_class = SystemConfigChinldernSerializer
    create_serializer_class = SystemConfigCreateSerializer
    retrieve_serializer_class = SystemConfigChinldernSerializer
    # filter_fields = ['id','parent']
    filter_class = SystemConfigFilter

    def save_content(self, request):
        body = request.data
        data_mapping = {item["id"]: item for item in body}
        for obj_id, data in data_mapping.items():
            instance_obj = SystemConfig.objects.filter(id=obj_id).first()
            if instance_obj is None:
                # return SystemConfig.objects.create(**data)
                serializer = SystemConfigCreateSerializer(data=data)
            else:
                serializer = SystemConfigCreateSerializer(instance_obj, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return DetailResponse(msg="success")

    def get_association_table(self, request):
        """ """
        res = [ele.get("table") for ele in get_all_models_objects().values()]
        return DetailResponse(msg="success", data=res)

    def get_table_data(self, request, pk):
        """ """
        instance = SystemConfig.objects.filter(id=pk).first()
        if instance is None:
            return ErrorResponse(msg="search error~")
        setting = instance.setting
        if setting is None:
            return ErrorResponse(msg="search error~")
        table = setting.get("table")
        model = get_all_models_objects(table).get("object", {})
        #
        queryset = model.objects.values()
        body = request.query_params
        search_value = body.get("search", None)
        if search_value:
            search_fields = setting.get("searchField")
            filters = Q()
            filters.connector = "OR"
            for item in search_fields:
                filed = "{0}__icontains".format(item.get("field"))
                filters.children.append((filed, search_value))
            queryset = model.objects.filter(filters).values()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(queryset)
        return SuccessResponse(msg="success", data=queryset, total=len(queryset))

    def get_relation_info(self, request):
        """ """
        body = request.query_params
        var_name = body.get("varName", None)
        table = body.get("table", None)
        instance = SystemConfig.objects.filter(
            key=var_name, setting__table=table
        ).first()
        if instance is None:
            return ErrorResponse(msg="no relation information obtained")
        relation_id = body.get("relationIds", None)
        relationIds = []
        if relation_id is None:
            return ErrorResponse(msg="no relation information obtained")
        if instance.form_item_type in [13]:
            relationIds = [relation_id]
        elif instance.form_item_type in [14]:
            relationIds = relation_id.split(",")
        queryset = SystemConfig.objects.filter(value__in=relationIds).first()
        if queryset is None:
            return ErrorResponse(msg="no relation information obtained")
        serializer = SystemConfigChinldernSerializer(queryset.parent)
        return DetailResponse(msg="success", data=serializer.data)


class InitSettingsViewSet(APIView):
    """ """

    authentication_classes = []
    permission_classes = []

    def filter_system_config_values(self, data: dict):
        """

        :param data:
        :return:
        """
        if not self.request.query_params.get("key", ""):
            return data
        new_data = {}
        for key in self.request.query_params.get("key", "").split("|"):
            if key:
                new_data.update(
                    **dict(filter(lambda x: x[0].startswith(key), data.items()))
                )
        return new_data

    def get(self, request):
        data = dispatch.get_system_config()
        if not data:
            dispatch.refresh_system_config()
            data = dispatch.get_system_config()
        #
        backend_config = [
            f"{ele.get('parent__key')}.{ele.get('key')}"
            for ele in SystemConfig.objects.filter(
                status=False, parent_id__isnull=False
            ).values("parent__key", "key")
        ]
        data = dict(filter(lambda x: x[0] not in backend_config, data.items()))
        data = self.filter_system_config_values(data=data)
        return DetailResponse(data=data)
