import hashlib

from django.contrib.auth.hashers import make_password
from django_restql.fields import DynamicSerializerMethodField
from rest_framework import serializers
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from application import dispatch
from dvadmin.system.models import Users, Role, Dept
from dvadmin.system.views.role import RoleSerializer
from dvadmin.utils.json_response import ErrorResponse, DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet


def recursion(instance, parent, result):
    new_instance = getattr(instance, parent, None)
    res = []
    data = getattr(instance, result, None)
    if data:
        res.append(data)
    if new_instance:
        array = recursion(new_instance, parent, result)
        res += array
    return res


class UserSerializer(CustomModelSerializer):
    """ """

    dept_name = serializers.CharField(source="dept.name", read_only=True)
    role_info = DynamicSerializerMethodField()
    dept_name_all = serializers.SerializerMethodField()

    class Meta:
        model = Users
        read_only_fields = ["id"]
        exclude = ["password"]
        extra_kwargs = {
            "post": {"required": False},
        }

    def get_dept_name_all(self, instance):
        dept_name_all = recursion(instance.dept, "parent", "name")
        dept_name_all.reverse()
        return "/".join(dept_name_all)

    def get_role_info(self, instance, parsed_query):
        roles = instance.role.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        serializer = RoleSerializer(roles, many=True, parsed_query=parsed_query)
        return serializer.data


class UsersInitSerializer(CustomModelSerializer):
    """ """

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        role_key = self.initial_data.get("role_key", [])
        role_ids = Role.objects.filter(key__in=role_key).values_list("id", flat=True)
        instance.role.set(role_ids)
        dept_key = self.initial_data.get("dept_key", None)
        dept_id = Dept.objects.filter(key=dept_key).first()
        instance.dept = dept_id
        instance.save()
        return instance

    class Meta:
        model = Users
        fields = [
            "username",
            "email",
            "mobile",
            "avatar",
            "name",
            "gender",
            "user_type",
            "dept",
            "user_type",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "creator",
            "dept_belong_id",
            "password",
            "last_login",
            "is_superuser",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True},
        }


class UserCreateSerializer(CustomModelSerializer):
    """ """

    username = serializers.CharField(
        max_length=50,
        validators=[
            CustomUniqueValidator(
                queryset=Users.objects.all(), message="account must be unique"
            )
        ],
    )
    password = serializers.CharField(
        required=False,
    )

    def validate_password(self, value):
        """ """
        password = self.initial_data.get("password")
        if password:
            return make_password(value)
        return value

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept_belong_id = data.dept_id
        data.save()
        data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            "post": {"required": False},
        }


class UserUpdateSerializer(CustomModelSerializer):
    """ """

    username = serializers.CharField(
        max_length=50,
        validators=[
            CustomUniqueValidator(
                queryset=Users.objects.all(), message="account must be unique"
            )
        ],
    )
    # password = serializers.CharField(required=False, allow_blank=True)
    mobile = serializers.CharField(
        max_length=50,
        validators=[
            CustomUniqueValidator(
                queryset=Users.objects.all(), message="mobile must be unique"
            )
        ],
        allow_blank=True,
    )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept_belong_id = data.dept_id
        data.save()
        data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = Users
        read_only_fields = ["id", "password"]
        fields = "__all__"
        extra_kwargs = {
            "post": {"required": False, "read_only": True},
        }


class UserInfoUpdateSerializer(CustomModelSerializer):
    """ """

    mobile = serializers.CharField(
        max_length=50,
        validators=[
            CustomUniqueValidator(
                queryset=Users.objects.all(), message="mobile must be unique"
            )
        ],
        allow_blank=True,
    )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Users
        fields = ["email", "mobile", "avatar", "name", "gender"]
        extra_kwargs = {
            "post": {"required": False, "read_only": True},
        }


class ExportUserProfileSerializer(CustomModelSerializer):
    """ """

    last_login = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True
    )
    is_active = serializers.SerializerMethodField(read_only=True)
    dept_name = serializers.CharField(source="dept.name", default="")
    dept_owner = serializers.CharField(source="dept.owner", default="")
    gender = serializers.CharField(source="get_gender_display", read_only=True)

    def get_is_active(self, instance):
        return "enable" if instance.is_active else "disable"

    class Meta:
        model = Users
        fields = (
            "username",
            "name",
            "email",
            "mobile",
            "gender",
            "is_active",
            "last_login",
            "dept_name",
            "dept_owner",
        )


class UserProfileImportSerializer(CustomModelSerializer):
    def save(self, **kwargs):
        data = super().save(**kwargs)
        password = hashlib.new(
            "md5", str(self.initial_data.get("password", "")).encode(encoding="UTF-8")
        ).hexdigest()
        data.set_password(password)
        data.save()
        return data

    class Meta:
        model = Users
        exclude = (
            "password",
            "post",
            "user_permissions",
            "groups",
            "is_superuser",
            "date_joined",
        )


class UserViewSet(CustomModelViewSet):
    """

    list:
    create:
    update:
    retrieve:
    destroy:
    """

    queryset = Users.objects.exclude(is_superuser=1).all()
    serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    update_serializer_class = UserUpdateSerializer
    # filter_fields = ["name", "username", "gender", "is_active", "dept", "user_type"]
    filter_fields = {
        "name": ["exact"],
        "mobile": ["exact"],
        "username": ["exact"],
        "gender": ["icontains"],
        "is_active": ["icontains"],
        "dept": ["exact"],
        "user_type": ["exact"],
    }
    search_fields = ["username", "name", "gender", "dept__name", "role__name"]
    # export
    export_field_label = {
        "username": "username",
        "name": "name",
        "email": "email",
        "mobile": "mobile",
        "gender": "gender",
        "is_active": "is_active",
        "last_login": "last_login",
        "dept_name": "dept_name",
        "dept_owner": "dept_owner",
    }
    export_serializer_class = ExportUserProfileSerializer
    # import
    import_serializer_class = UserProfileImportSerializer
    import_field_dict = {
        "username": "username",
        "name": "name",
        "email": "email",
        "mobile": "mobile",
        "gender": {
            "title": "gender",
            "choices": {
                "data": {"unknown": 2, "male": 1, "female": 0},
            },
        },
        "is_active": {
            "title": "is active",
            "choices": {
                "data": {"enable": True, "disable": False},
            },
        },
        "password": "password",
        "dept": {
            "title": "department",
            "choices": {
                "queryset": Dept.objects.filter(status=True),
                "values_name": "name",
            },
        },
        "role": {
            "title": "role",
            "choices": {
                "queryset": Role.objects.filter(status=True),
                "values_name": "name",
            },
        },
    }

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def user_info(self, request):
        """"""
        user = request.user
        result = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "mobile": user.mobile,
            "user_type": user.user_type,
            "gender": user.gender,
            "email": user.email,
            "avatar": user.avatar,
            "dept": user.dept_id,
            "is_superuser": user.is_superuser,
            "role": user.role.values_list("id", flat=True),
        }
        if hasattr(connection, "tenant"):
            result["tenant_id"] = connection.tenant and connection.tenant.id
            result["tenant_name"] = connection.tenant and connection.tenant.name
        dept = getattr(user, "dept", None)
        if dept:
            result["dept_info"] = {"dept_id": dept.id, "dept_name": dept.name}
        role = getattr(user, "role", None)
        if role:
            result["role_info"] = role.values("id", "name", "key")
        return DetailResponse(data=result, msg="success")

    @action(methods=["PUT"], detail=False, permission_classes=[IsAuthenticated])
    def update_user_info(self, request):
        """"""
        serializer = UserInfoUpdateSerializer(
            request.user, data=request.data, request=request
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return DetailResponse(data=None, msg="updated")

    @action(methods=["PUT"], detail=True, permission_classes=[IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        """"""
        data = request.data
        old_pwd = data.get("oldPassword")
        new_pwd = data.get("newPassword")
        new_pwd2 = data.get("newPassword2")
        if old_pwd is None or new_pwd is None or new_pwd2 is None:
            return ErrorResponse(msg="parameter cannot be empty")
        if new_pwd != new_pwd2:
            return ErrorResponse(msg="two passwords do not match")
        check_password = request.user.check_password(old_pwd)
        if not check_password:
            check_password = request.user.check_password(
                hashlib.md5(old_pwd.encode(encoding="UTF-8")).hexdigest()
            )
        if check_password:
            request.user.password = make_password(new_pwd)
            request.user.save()
            return DetailResponse(data=None, msg="success")
        else:
            return ErrorResponse(msg="incorrect old password")

    @action(methods=["PUT"], detail=True, permission_classes=[IsAuthenticated])
    def reset_to_default_password(self, request, *args, **kwargs):
        """"""
        instance = Users.objects.filter(id=kwargs.get("pk")).first()
        if instance:
            instance.set_password(
                dispatch.get_system_config_values("base.default_password")
            )
            instance.save()
            return DetailResponse(data=None, msg="reset password success")
        else:
            return ErrorResponse(msg="user not obtained")

    @action(methods=["PUT"], detail=True)
    def reset_password(self, request, pk):
        """ """
        instance = Users.objects.filter(id=pk).first()
        data = request.data
        new_pwd = data.get("newPassword")
        new_pwd2 = data.get("newPassword2")
        if instance:
            if new_pwd != new_pwd2:
                return ErrorResponse(msg="two passwords do not match")
            else:
                instance.password = make_password(new_pwd)
                instance.save()
                return DetailResponse(data=None, msg="updated")
        else:
            return ErrorResponse(msg="user not obtained")
