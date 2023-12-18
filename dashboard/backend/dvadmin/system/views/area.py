# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers

from dvadmin.system.models import Area
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class AreaSerializer(CustomModelSerializer):
    """ """

    pcode_count = serializers.SerializerMethodField(read_only=True)

    def get_pcode_count(self, instance: Area):
        return Area.objects.filter(pcode=instance).count()

    class Meta:
        model = Area
        fields = "__all__"
        read_only_fields = ["id"]


class AreaCreateUpdateSerializer(CustomModelSerializer):
    """ """

    class Meta:
        model = Area
        fields = "__all__"


class AreaViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    extra_filter_backends = []
