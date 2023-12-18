# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/1 001 22:57
@Remark: custom viewset
"""
import uuid

from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.filters import DataLevelPermissionsFilter
from dvadmin.utils.import_export_mixin import (
    ExportSerializerMixin,
    ImportSerializerMixin,
)
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse, DetailResponse
from dvadmin.utils.permission import CustomPermission
from django_restql.mixins import QueryArgumentsMixin


class CustomModelViewSet(
    ModelViewSet, ImportSerializerMixin, ExportSerializerMixin, QueryArgumentsMixin
):
    """
    Custom ModelViewSet:
    Unified and standardized return format; create, search, and update can use different serializers
    (1)ORM performance optimization, using values as much as possible Queryset form
    (2)xxx_serializer_class (xxx=create|update|list|retrieve|destroy)
    (3)filter_fields = '__all__' Default support for field queries in all models (except for JSON fields)
    (4)import_field_dict={}  {model: model's label}
    (5)export_field_label = []
    """

    values_queryset = None
    ordering_fields = "__all__"
    create_serializer_class = None
    update_serializer_class = None
    filter_fields = "__all__"
    search_fields = ()
    extra_filter_backends = [DataLevelPermissionsFilter]
    permission_classes = [CustomPermission]
    import_field_dict = {}
    export_field_label = {}

    def filter_queryset(self, queryset):
        for backend in set(
            set(self.filter_backends) | set(self.extra_filter_backends or [])
        ):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        if getattr(self, "values_queryset", None):
            return self.values_queryset
        return super().get_queryset()

    def get_serializer_class(self):
        action_serializer_name = f"{self.action}_serializer_class"
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    # Directly modify the existing API through many=True to enable batch creation
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        if isinstance(self.request.data, list):
            with transaction.atomic():
                return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="create succeed")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="get succeed")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DetailResponse(data=serializer.data, msg="get succeed")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, request=request, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return DetailResponse(data=serializer.data, msg="update succeed")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return DetailResponse(data=[], msg="delete succeed")

    keys = openapi.Schema(
        description="id list", type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING
    )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, required=["keys"], properties={"keys": keys}
        ),
        operation_summary="batch delete",
    )
    @action(methods=["delete"], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        request_data = request.data
        keys = request_data.get("keys", None)
        if keys:
            self.get_queryset().filter(id__in=keys).delete()
            return SuccessResponse(data=[], msg="delete succeed")
        else:
            return ErrorResponse(msg="no keys obtained")
