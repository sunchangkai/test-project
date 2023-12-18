# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/3 003 0:30
@Remark: 角色管理
"""
from rest_framework import serializers
from rest_framework.decorators import action

from dvadmin.system.models import Role, Menu
from dvadmin.system.views.dept import DeptSerializer
from dvadmin.system.views.menu import MenuSerializer
from dvadmin.system.views.menu_button import MenuButtonSerializer
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet


class RoleSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]


class RoleInitSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = Role
        fields = [
            "name",
            "key",
            "sort",
            "status",
            "admin",
            "data_range",
            "remark",
            "creator",
            "dept_belong_id",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True},
        }


class RoleCreateUpdateSerializer(CustomModelSerializer):
    """ """

    menu = MenuSerializer(many=True, read_only=True)
    dept = DeptSerializer(many=True, read_only=True)
    permission = MenuButtonSerializer(many=True, read_only=True)
    key = serializers.CharField(
        max_length=50,
        validators=[
            CustomUniqueValidator(
                queryset=Role.objects.all(), message="Permission must be unique"
            )
        ],
    )
    name = serializers.CharField(
        max_length=50, validators=[CustomUniqueValidator(queryset=Role.objects.all())]
    )

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept.set(self.initial_data.get("dept", []))
        data.menu.set(self.initial_data.get("menu", []))
        data.permission.set(self.initial_data.get("permission", []))
        return data

    class Meta:
        model = Role
        fields = "__all__"


class MenuPermissonSerializer(CustomModelSerializer):
    """ """

    menuPermission = MenuButtonSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = "__all__"


class RoleViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer

    @action(methods=["GET"], detail=True, permission_classes=[])
    def roleId_get_menu(self, request, *args, **kwargs):
        """"""
        # instance = self.get_object()
        # queryset = instance.menu.all()
        queryset = Menu.objects.filter(status=1).all()
        serializer = MenuPermissonSerializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)
