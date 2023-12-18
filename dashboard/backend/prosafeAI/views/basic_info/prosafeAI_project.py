from django.shortcuts import render

# Create your views here.
from rest_framework import serializers

from prosafeAI.models import ProsafeAIProject
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProsafeAIProjectSerializer(CustomModelSerializer):
    """
    project-serializer
    """

    # pcode_count = serializers.SerializerMethodField(read_only=True)
    #
    # def get_pcode_count(self, instance: Area):
    #     return Area.objects.filter(pcode=instance).count()

    class Meta:
        model = ProsafeAIProject
        fields = "__all__"
        read_only_fields = ["id"]


class ProsafeAIProjectCreateUpdateSerializer(CustomModelSerializer):
    """
    project create/update serializer
    """

    class Meta:
        model = ProsafeAIProject
        fields = "__all__"


class ProsafeAIProjectViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = ProsafeAIProject.objects.all()
    serializer_class = ProsafeAIProjectSerializer
    extra_filter_backends = []
