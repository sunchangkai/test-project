# -*- coding: utf-8 -*-
import json
from django_restql.fields import DynamicSerializerMethodField
from rest_framework import serializers
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from application.websocketConfig import websocket_push
from dvadmin.system.models import MessageCenter, Users, MessageCenterTargetUser
from dvadmin.system.views.dept import DeptSerializer
from dvadmin.system.views.role import RoleSerializer
from dvadmin.system.views.user import UserSerializer
from dvadmin.utils.json_response import SuccessResponse, DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class MessageCenterSerializer(CustomModelSerializer):
    """ """

    role_info = DynamicSerializerMethodField()
    user_info = DynamicSerializerMethodField()
    dept_info = DynamicSerializerMethodField()
    is_read = serializers.BooleanField(read_only=True, source="target_user__is_read")

    def get_role_info(self, instance, parsed_query):
        roles = instance.target_role.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        serializer = RoleSerializer(roles, many=True, parsed_query=parsed_query)
        return serializer.data

    def get_user_info(self, instance, parsed_query):
        users = instance.target_user.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        serializer = UserSerializer(users, many=True, parsed_query=parsed_query)
        return serializer.data

    def get_dept_info(self, instance, parsed_query):
        dept = instance.target_dept.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        serializer = DeptSerializer(dept, many=True, parsed_query=parsed_query)
        return serializer.data

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterTargetUserSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = MessageCenterTargetUser
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterTargetUserListSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = MessageCenterTargetUser
        fields = "__all__"
        read_only_fields = ["id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["title"] = instance.messagecenter.title
        data["content"] = instance.messagecenter.content
        data["target_type"] = instance.messagecenter.target_type
        data["id"] = instance.messagecenter.id
        return data


class MessageCenterCreateSerializer(CustomModelSerializer):
    """ """

    def save(self, **kwargs):
        data = super().save(**kwargs)
        initial_data = self.initial_data
        target_type = initial_data.get("target_type")
        # identify and save the target user based on the target type
        users = initial_data.get("target_user", [])
        if target_type in [1]:  # role
            target_role = initial_data.get("target_role")
            users = (
                Users.objects.exclude(is_deleted=True)
                .filter(role__id__in=target_role)
                .values_list("id", flat=True)
            )
        if target_type in [2]:  # department
            target_dept = initial_data.get("target_dept")
            users = (
                Users.objects.exclude(is_deleted=True)
                .filter(dept__id__in=target_dept)
                .values_list("id", flat=True)
            )
        if target_type in [3]:  # system message
            users = Users.objects.exclude(is_deleted=True).values_list("id", flat=True)
        targetuser_data = []
        for user in users:
            targetuser_data.append({"messagecenter": data.id, "users": user})
        targetuser_instance = MessageCenterTargetUserSerializer(
            data=targetuser_data, many=True, request=self.request
        )
        targetuser_instance.is_valid(raise_exception=True)
        targetuser_instance.save()
        for user in users:
            unread_count = MessageCenterTargetUser.objects.filter(
                users__id=user, is_read=False
            ).count()
            websocket_push(
                user,
                {
                    "sender": "system",
                    "contentType": "TEXT",
                    "content": {"model": "message_center", "unread": unread_count},
                },
            )
        return data

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = MessageCenter.objects.order_by("create_datetime")
    serializer_class = MessageCenterSerializer
    create_serializer_class = MessageCenterCreateSerializer
    extra_filter_backends = []

    def get_queryset(self):
        if self.action == "list":
            return MessageCenter.objects.filter(creator=self.request.user.id).all()
        return MessageCenter.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """ """
        pk = kwargs.get("pk")
        user_id = self.request.user.id
        queryset = MessageCenterTargetUser.objects.filter(
            users__id=user_id, messagecenter__id=pk
        ).first()
        if queryset:
            queryset.is_read = True
            queryset.save()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # push message
        unread_count = MessageCenterTargetUser.objects.filter(
            users__id=user_id, is_read=False
        ).count()
        websocket_push(
            user_id,
            {
                "sender": "system",
                "contentType": "TEXT",
                "content": {"model": "message_center", "unread": unread_count},
            },
        )
        return DetailResponse(data=serializer.data, msg="success")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def get_self_receive(self, request):
        """ """
        self_user_id = self.request.user.id
        queryset = MessageCenterTargetUser.objects.filter(
            users__id=self_user_id
        ).order_by("-create_datetime")
        # queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MessageCenterTargetUserListSerializer(
                page, many=True, request=request
            )
            return self.get_paginated_response(serializer.data)
        serializer = MessageCenterTargetUserListSerializer(
            queryset, many=True, request=request
        )
        return SuccessResponse(data=serializer.data, msg="success")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def get_newest_msg(self, request):
        """ """
        self_user_id = self.request.user.id
        queryset = (
            MessageCenterTargetUser.objects.filter(users__id=self_user_id)
            .order_by("create_datetime")
            .last()
        )
        data = None
        if queryset:
            serializer = MessageCenterTargetUserListSerializer(
                queryset, many=False, request=request
            )
            data = serializer.data
        return DetailResponse(data=data, msg="success")
