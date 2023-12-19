from rest_framework import serializers

from dvadmin.system.models import FileList
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        return "media/" + str(instance.url)

    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):
        validated_data["name"] = str(self.initial_data.get("file"))
        validated_data["url"] = self.initial_data.get("file")
        return super().create(validated_data)


class FileViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = FileList.objects.all()
    serializer_class = FileSerializer
    filter_fields = [
        "name",
    ]
    permission_classes = []