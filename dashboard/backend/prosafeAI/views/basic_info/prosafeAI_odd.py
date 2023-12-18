from django.shortcuts import render

# Create your views here.
from rest_framework import serializers

from prosafeAI.models import ProsafeAIOdd
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProsafeAIOddSerializer(CustomModelSerializer):
    """
    odd-serializer
    """

    # pcode_count = serializers.SerializerMethodField(read_only=True)
    #
    # def get_pcode_count(self, instance: Area):
    #     return Area.objects.filter(pcode=instance).count()

    class Meta:
        model = ProsafeAIOdd
        fields = "__all__"
        read_only_fields = ["id"]


class ProsafeAIOddCreateUpdateSerializer(CustomModelSerializer):
    """
    odd create/update serializer
    """

    class Meta:
        model = ProsafeAIOdd
        fields = "__all__"


class ProsafeAIOddViewSet(CustomModelViewSet):
    """
    odd manage interface
    list
    create
    update
    retrieve
    destroy
    """

    queryset = ProsafeAIOdd.objects.all()
    serializer_class = ProsafeAIOddSerializer
    extra_filter_backends = []
