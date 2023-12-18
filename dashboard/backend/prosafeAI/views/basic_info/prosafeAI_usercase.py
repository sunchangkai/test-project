from django.shortcuts import render

# Create your views here.
from rest_framework import serializers

from prosafeAI.models import ProsafeAIUsercase
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProsafeAIUsercaseSerializer(CustomModelSerializer):
    """
    usercase-serializer
    """

    # pcode_count = serializers.SerializerMethodField(read_only=True)
    #
    # def get_pcode_count(self, instance: Area):
    #     return Area.objects.filter(pcode=instance).count()

    class Meta:
        model = ProsafeAIUsercase
        fields = "__all__"
        read_only_fields = ["id"]


class ProsafeAIUsercaseCreateUpdateSerializer(CustomModelSerializer):
    """
    usercase create/update serializer
    """

    class Meta:
        model = ProsafeAIUsercase
        fields = "__all__"


class ProsafeAIUsercaseViewSet(CustomModelViewSet):
    """

    list:
    create:
    update
    retrieve:
    destroy:
    """

    queryset = ProsafeAIUsercase.objects.all()
    serializer_class = ProsafeAIUsercaseSerializer
    extra_filter_backends = []
