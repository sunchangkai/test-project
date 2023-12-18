from django.shortcuts import render

# Create your views here.
from rest_framework import serializers

from prosafeAI.models import ProsafeAIField
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProsafeAIFieldSerializer(CustomModelSerializer):
    """
    field-serializer
    """

    # pcode_count = serializers.SerializerMethodField(read_only=True)
    #
    # def get_pcode_count(self, instance: Area):
    #     return Area.objects.filter(pcode=instance).count()

    class Meta:
        model = ProsafeAIField
        fields = "__all__"
        read_only_fields = ["id"]


class ProsafeAIFieldCreateUpdateSerializer(CustomModelSerializer):
    """
    field create/update serializer
    """

    class Meta:
        model = ProsafeAIField
        fields = "__all__"


class ProsafeAIFieldViewSet(CustomModelViewSet):
    """
    field manage interface
    list:
    create
    update:
    retrieve:
    destroy:
    """

    queryset = ProsafeAIField.objects.all()
    serializer_class = ProsafeAIFieldSerializer
    extra_filter_backends = []
