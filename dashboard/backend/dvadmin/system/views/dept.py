# -*- coding: utf-8 -*-

"""
@author: H0nGzA1
@contact: QQ:2505811377
@Remark:
"""
from rest_framework import serializers
from rest_framework.decorators import action

from dvadmin.system.models import Dept
from dvadmin.utils.json_response import DetailResponse, SuccessResponse
from dvadmin.utils.permission import AnonymousUserPermission
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class DeptSerializer(CustomModelSerializer):
    """ """

    parent_name = serializers.CharField(read_only=True, source="parent.name")
    status_label = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()

    def get_status_label(self, obj: Dept):
        if obj.status:
            return "enable"
        return "disable"

    def get_has_children(self, obj: Dept):
        return Dept.objects.filter(parent_id=obj.id).count()

    class Meta:
        model = Dept
        fields = "__all__"
        read_only_fields = ["id"]


class DeptImportSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = Dept
        fields = "__all__"
        read_only_fields = ["id"]


class DeptInitSerializer(CustomModelSerializer):
    """ """

    children = serializers.SerializerMethodField()

    def get_children(self, obj: Dept):
        data = []
        instance = Dept.objects.filter(parent_id=obj.id)
        if instance:
            serializer = DeptInitSerializer(instance=instance, many=True)
            data = serializer.data
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        children = self.initial_data.get("children")
        if children:
            for menu_data in children:
                menu_data["parent"] = instance.id
                filter_data = {
                    "name": menu_data["name"],
                    "parent": menu_data["parent"],
                    "key": menu_data["key"],
                }
                instance_obj = Dept.objects.filter(**filter_data).first()
                if instance_obj and not self.initial_data.get("reset"):
                    continue
                serializer = DeptInitSerializer(
                    instance_obj, data=menu_data, request=self.request
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return instance

    class Meta:
        model = Dept
        fields = [
            "name",
            "sort",
            "owner",
            "phone",
            "email",
            "status",
            "parent",
            "creator",
            "dept_belong_id",
            "children",
            "key",
        ]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True},
        }
        read_only_fields = ["id", "children"]


class DeptCreateUpdateSerializer(CustomModelSerializer):
    """ """

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.dept_belong_id = instance.id
        instance.save()
        return instance

    class Meta:
        model = Dept
        fields = "__all__"


class DeptViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    create_serializer_class = DeptCreateUpdateSerializer
    update_serializer_class = DeptCreateUpdateSerializer
    filter_fields = ["name", "id", "parent"]
    search_fields = []
    # extra_filter_backends = []
    import_serializer_class = DeptImportSerializer
    import_field_dict = {
        "name": "department name",
        "key": "department key",
    }

    def list(self, request, *args, **kwargs):
        # if lazy，return parent
        queryset = self.filter_queryset(self.get_queryset())
        lazy = self.request.query_params.get("lazy")
        parent = self.request.query_params.get("parent")
        if lazy:
            #
            if not parent:
                role_list = request.user.role.filter(status=1).values(
                    "admin", "data_range"
                )
                is_admin = False
                for ele in role_list:
                    if 3 == ele.get("data_range") or ele.get("admin"):
                        is_admin = True
                        break
                if self.request.user.is_superuser or is_admin:
                    queryset = queryset.filter(parent__isnull=True)
                else:
                    queryset = queryset.filter(id=self.request.user.dept_id)
            serializer = self.get_serializer(queryset, many=True, request=request)
            return SuccessResponse(data=serializer.data, msg="success")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="success")

    def dept_lazy_tree(self, request, *args, **kwargs):
        parent = self.request.query_params.get("parent")
        queryset = self.filter_queryset(self.get_queryset())
        if not parent:
            if self.request.user.is_superuser:
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(id=self.request.user.dept_id)
        data = (
            queryset.filter(status=True).order_by("sort").values("name", "id", "parent")
        )
        return DetailResponse(data=data, msg="success")

    @action(methods=["GET"], detail=False, permission_classes=[AnonymousUserPermission])
    def all_dept(self, request, *args, **kwargs):
        self.extra_filter_backends = []
        queryset = self.filter_queryset(self.get_queryset())
        data = (
            queryset.filter(status=True).order_by("sort").values("name", "id", "parent")
        )
        return DetailResponse(data=data, msg="success")
