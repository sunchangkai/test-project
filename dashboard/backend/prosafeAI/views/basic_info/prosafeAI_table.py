from django.shortcuts import render

# Create your views here.
from rest_framework import serializers

from prosafeAI.models import ProsafeAITable
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProsafeAITableSerializer(CustomModelSerializer):
    """
    table-serializer
    """

    # pcode_count = serializers.SerializerMethodField(read_only=True)
    #
    # def get_pcode_count(self, instance: Area):
    #     return Area.objects.filter(pcode=instance).count()

    class Meta:
        model = ProsafeAITable
        fields = "__all__"
        read_only_fields = ["id"]


class ProsafeAITableCreateUpdateSerializer(CustomModelSerializer):
    """
    table create/update serializer
    """

    class Meta:
        model = ProsafeAITable
        fields = "__all__"


class ProsafeAITableViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = ProsafeAITable.objects.all()
    serializer_class = ProsafeAITableSerializer
    extra_filter_backends = []
