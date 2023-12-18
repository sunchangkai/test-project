import hashlib
import os

from django.contrib.auth.models import AbstractUser
from django.db import models

from application import dispatch
from dvadmin.utils.models import CoreModel, table_prefix

STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
)


class Users(CoreModel, AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name="username",
        help_text="username",
    )
    email = models.EmailField(
        max_length=255, verbose_name="email", null=True, blank=True, help_text="email"
    )
    mobile = models.CharField(
        max_length=255, verbose_name="mobile", null=True, blank=True, help_text="mobile"
    )
    avatar = models.CharField(
        max_length=255, verbose_name="avatar", null=True, blank=True, help_text="avatar"
    )
    name = models.CharField(max_length=40, verbose_name="name", help_text="name")
    GENDER_CHOICES = (
        (0, "unknown"),
        (1, "male"),
        (2, "female"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES,
        default=0,
        verbose_name="gender",
        null=True,
        blank=True,
        help_text="gender",
    )
    USER_TYPE = (
        (0, "backend user"),
        (1, "frontend user"),
    )
    user_type = models.IntegerField(
        choices=USER_TYPE,
        default=0,
        verbose_name="user_type",
        null=True,
        blank=True,
        help_text="user_type",
    )
    post = models.ManyToManyField(
        to="Post",
        blank=True,
        verbose_name="post",
        db_constraint=False,
        help_text="post",
    )
    role = models.ManyToManyField(
        to="Role",
        blank=True,
        verbose_name="role",
        db_constraint=False,
        help_text="role",
    )
    dept = models.ForeignKey(
        to="Dept",
        verbose_name="department",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="department",
    )

    def set_password(self, raw_password):
        super().set_password(
            hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest()
        )

    class Meta:
        db_table = table_prefix + "system_users"
        verbose_name = "user table"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Post(CoreModel):
    name = models.CharField(
        null=False, max_length=64, verbose_name="name", help_text="name"
    )
    code = models.CharField(max_length=32, verbose_name="code", help_text="code")
    sort = models.IntegerField(default=1, verbose_name="sort", help_text="sort")
    STATUS_CHOICES = (
        (0, "leave"),
        (1, "in-service"),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES, default=1, verbose_name="status", help_text="status"
    )

    class Meta:
        db_table = table_prefix + "system_post"
        verbose_name = "post table"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Role(CoreModel):
    name = models.CharField(max_length=64, verbose_name="name", help_text="name")
    key = models.CharField(
        max_length=64, unique=True, verbose_name="key", help_text="key"
    )
    sort = models.IntegerField(default=1, verbose_name="sort", help_text="sort")
    status = models.BooleanField(
        default=True, verbose_name="status", help_text="status"
    )
    admin = models.BooleanField(
        default=False, verbose_name="admin or not", help_text="admin or not"
    )
    DATASCOPE_CHOICES = (
        (0, "Only personal data permission"),
        (1, "Data permissions for this department and below"),
        (2, "Data permissions of this department"),
        (3, "All data permissions"),
        (4, "custom data permissions"),
    )
    data_range = models.IntegerField(
        default=0,
        choices=DATASCOPE_CHOICES,
        verbose_name="data_range",
        help_text="data_range",
    )
    remark = models.TextField(
        verbose_name="remark", help_text="remark", null=True, blank=True
    )
    dept = models.ManyToManyField(
        to="Dept",
        verbose_name="department",
        db_constraint=False,
        help_text="department",
    )
    menu = models.ManyToManyField(
        to="Menu", verbose_name="menu", db_constraint=False, help_text="menu"
    )
    permission = models.ManyToManyField(
        to="MenuButton",
        verbose_name="permission",
        db_constraint=False,
        help_text="permission",
    )

    class Meta:
        db_table = table_prefix + "system_role"
        verbose_name = "role table"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Dept(CoreModel):
    name = models.CharField(max_length=64, verbose_name="name", help_text="name")
    key = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        verbose_name="key",
        help_text="key",
    )
    sort = models.IntegerField(default=1, verbose_name="sort", help_text="sort")
    owner = models.CharField(
        max_length=32, verbose_name="owner", null=True, blank=True, help_text="owner"
    )
    phone = models.CharField(
        max_length=32, verbose_name="phone", null=True, blank=True, help_text="phone"
    )
    email = models.EmailField(
        max_length=32, verbose_name="email", null=True, blank=True, help_text="email"
    )
    status = models.BooleanField(
        default=True, verbose_name="status", null=True, blank=True, help_text="status"
    )
    parent = models.ForeignKey(
        to="Dept",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="parent department",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="parent department",
    )

    class Meta:
        db_table = table_prefix + "system_dept"
        verbose_name = "department table"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Menu(CoreModel):
    parent = models.ForeignKey(
        to="Menu",
        on_delete=models.CASCADE,
        verbose_name="parent menu",
        null=True,
        blank=True,
        db_constraint=False,
        help_text="parent menu",
    )
    icon = models.CharField(
        max_length=64, verbose_name="icon", null=True, blank=True, help_text="icon"
    )
    name = models.CharField(max_length=64, verbose_name="name", help_text="name")
    sort = models.IntegerField(
        default=1, verbose_name="sort", null=True, blank=True, help_text="sort"
    )
    ISLINK_CHOICES = (
        (0, "no"),
        (1, "yes"),
    )
    is_link = models.BooleanField(
        default=False, verbose_name="is_link", help_text="is_link"
    )
    is_catalog = models.BooleanField(
        default=False, verbose_name="is_catalog", help_text="is_catalog"
    )
    web_path = models.CharField(
        max_length=128,
        verbose_name="web_path",
        null=True,
        blank=True,
        help_text="web_path",
    )
    component = models.CharField(
        max_length=128,
        verbose_name="component",
        null=True,
        blank=True,
        help_text="component",
    )
    component_name = models.CharField(
        max_length=50,
        verbose_name="component_name",
        null=True,
        blank=True,
        help_text="component_name",
    )
    status = models.BooleanField(
        default=True, blank=True, verbose_name="status", help_text="status"
    )
    cache = models.BooleanField(
        default=False, blank=True, verbose_name="cache", help_text="cache"
    )
    visible = models.BooleanField(
        default=True, blank=True, verbose_name="visible", help_text="visible"
    )

    class Meta:
        db_table = table_prefix + "system_menu"
        verbose_name = "menu table"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class MenuButton(CoreModel):
    menu = models.ForeignKey(
        to="Menu",
        db_constraint=False,
        related_name="menuPermission",
        on_delete=models.CASCADE,
        verbose_name="menu",
        help_text="menu",
    )
    name = models.CharField(max_length=64, verbose_name="name", help_text="name")
    value = models.CharField(max_length=64, verbose_name="value", help_text="value")
    api = models.CharField(max_length=200, verbose_name="api", help_text="api")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(
        default=0, verbose_name="method", null=True, blank=True, help_text="method"
    )

    class Meta:
        db_table = table_prefix + "system_menu_button"
        verbose_name = "menu button table"
        verbose_name_plural = verbose_name
        ordering = ("-name",)


class Dictionary(CoreModel):
    TYPE_LIST = (
        (0, "text"),
        (1, "number"),
        (2, "date"),
        (3, "datetime"),
        (4, "time"),
        (5, "files"),
        (6, "boolean"),
        (7, "images"),
    )
    label = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="label", help_text="label"
    )
    value = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="value", help_text="value"
    )
    parent = models.ForeignKey(
        to="self",
        related_name="sublist",
        db_constraint=False,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="parent",
        help_text="parent",
    )
    type = models.IntegerField(
        choices=TYPE_LIST, default=0, verbose_name="type", help_text="type"
    )
    color = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="color", help_text="color"
    )
    is_value = models.BooleanField(
        default=False, verbose_name="is_value", help_text="is_value"
    )
    status = models.BooleanField(
        default=True, verbose_name="status", help_text="status"
    )
    sort = models.IntegerField(
        default=1, verbose_name="sort", null=True, blank=True, help_text="sort"
    )
    remark = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name="remark",
        help_text="remark",
    )

    class Meta:
        db_table = table_prefix + "system_dictionary"
        verbose_name = "dictionary table"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_dictionary()  #

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_dictionary()
        return res


class OperationLog(CoreModel):
    request_modular = models.CharField(
        max_length=64,
        verbose_name="request_modular",
        null=True,
        blank=True,
        help_text="request_modular",
    )
    request_path = models.CharField(
        max_length=400,
        verbose_name="request_path",
        null=True,
        blank=True,
        help_text="request_path",
    )
    request_body = models.TextField(
        verbose_name="request_body", null=True, blank=True, help_text="request_body"
    )
    request_method = models.CharField(
        max_length=8,
        verbose_name="request_method",
        null=True,
        blank=True,
        help_text="request_method",
    )
    request_msg = models.TextField(
        verbose_name="request_message",
        null=True,
        blank=True,
        help_text="request_message",
    )
    request_ip = models.CharField(
        max_length=32,
        verbose_name="request_ip",
        null=True,
        blank=True,
        help_text="request_ip",
    )
    request_browser = models.CharField(
        max_length=64,
        verbose_name="request_browser",
        null=True,
        blank=True,
        help_text="request_browser",
    )
    response_code = models.CharField(
        max_length=32,
        verbose_name="response_code",
        null=True,
        blank=True,
        help_text="response_code",
    )
    request_os = models.CharField(
        max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统"
    )
    json_result = models.TextField(
        verbose_name="json_result", null=True, blank=True, help_text="json_result"
    )
    status = models.BooleanField(
        default=False, verbose_name="status", help_text="status"
    )

    class Meta:
        db_table = table_prefix + "system_operation_log"
        verbose_name = "operation log"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join("files", h[0:1], h[1:2], h + ext.lower())


class FileList(CoreModel):
    name = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="name", help_text="name"
    )
    url = models.FileField(upload_to=media_file_name)
    md5sum = models.CharField(
        max_length=36, blank=True, verbose_name="md5", help_text="md5"
    )

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.url.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super(FileList, self).save(*args, **kwargs)

    class Meta:
        db_table = table_prefix + "system_file_list"
        verbose_name = "file table"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Area(CoreModel):
    name = models.CharField(max_length=100, verbose_name="名称", help_text="名称")
    code = models.CharField(
        max_length=20, verbose_name="code", help_text="code", unique=True, db_index=True
    )
    level = models.BigIntegerField(
        verbose_name="level(1 province 2 city 3 county 4 township)",
        help_text="level(1 province 2 city 3 county 4 township)",
    )
    pinyin = models.CharField(max_length=255, verbose_name="pinyin", help_text="pinyin")
    initials = models.CharField(
        max_length=20, verbose_name="initials", help_text="initials"
    )
    enable = models.BooleanField(
        default=True, verbose_name="enable", help_text="enable"
    )
    pcode = models.ForeignKey(
        to="self",
        verbose_name="parent code",
        to_field="code",
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="parent code",
    )

    class Meta:
        db_table = table_prefix + "system_area"
        verbose_name = "area table"
        verbose_name_plural = verbose_name
        ordering = ("code",)

    def __str__(self):
        return f"{self.name}"


class ApiWhiteList(CoreModel):
    url = models.CharField(max_length=200, help_text="url", verbose_name="url")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(
        default=0, verbose_name="method", null=True, blank=True, help_text="method"
    )
    enable_datasource = models.BooleanField(
        default=True,
        verbose_name="enable_datasource",
        help_text="enable_datasource",
        blank=True,
    )

    class Meta:
        db_table = table_prefix + "api_white_list"
        verbose_name = "api white list"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class SystemConfig(CoreModel):
    parent = models.ForeignKey(
        to="self",
        verbose_name="parent",
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="parent",
    )
    title = models.CharField(max_length=50, verbose_name="title", help_text="title")
    key = models.CharField(
        max_length=20, verbose_name="key", help_text="key", db_index=True
    )
    value = models.JSONField(
        max_length=100, verbose_name="value", help_text="value", null=True, blank=True
    )
    sort = models.IntegerField(
        default=0, verbose_name="sort", help_text="sort", blank=True
    )
    status = models.BooleanField(
        default=True, verbose_name="status", help_text="status"
    )
    data_options = models.JSONField(
        verbose_name="data_options", help_text="data_options", null=True, blank=True
    )
    FORM_ITEM_TYPE_LIST = (
        (0, "text"),
        (1, "datetime"),
        (2, "date"),
        (3, "textarea"),
        (4, "select"),
        (5, "checkbox"),
        (6, "radio"),
        (7, "img"),
        (8, "file"),
        (9, "switch"),
        (10, "number"),
        (11, "array"),
        (12, "imgs"),
        (13, "foreignkey"),
        (14, "manytomany"),
        (15, "time"),
    )
    form_item_type = models.IntegerField(
        choices=FORM_ITEM_TYPE_LIST,
        verbose_name="type",
        help_text="type",
        default=0,
        blank=True,
    )
    rule = models.JSONField(
        null=True, blank=True, verbose_name="rule", help_text="校验规则"
    )
    placeholder = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="placeholder",
        help_text="placeholder",
    )
    setting = models.JSONField(
        null=True, blank=True, verbose_name="setting", help_text="setting"
    )

    class Meta:
        db_table = table_prefix + "system_config"
        verbose_name = "system config table"
        verbose_name_plural = verbose_name
        ordering = ("sort",)
        unique_together = (("key", "parent_id"),)

    def __str__(self):
        return f"{self.title}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_system_config()  # 有更新则刷新系统配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_system_config()
        return res


class LoginLog(CoreModel):
    LOGIN_TYPE_CHOICES = (
        (1, "normal"),
        (2, "Scan Code"),
    )
    username = models.CharField(
        max_length=32,
        verbose_name="username",
        null=True,
        blank=True,
        help_text="username",
    )
    ip = models.CharField(
        max_length=32, verbose_name="ip", null=True, blank=True, help_text="ip"
    )
    agent = models.TextField(
        verbose_name="agent", null=True, blank=True, help_text="agent"
    )
    browser = models.CharField(
        max_length=200,
        verbose_name="browser",
        null=True,
        blank=True,
        help_text="browser",
    )
    os = models.CharField(
        max_length=200, verbose_name="os", null=True, blank=True, help_text="os"
    )
    continent = models.CharField(
        max_length=50,
        verbose_name="continent",
        null=True,
        blank=True,
        help_text="continent",
    )
    country = models.CharField(
        max_length=50,
        verbose_name="country",
        null=True,
        blank=True,
        help_text="country",
    )
    province = models.CharField(
        max_length=50,
        verbose_name="province",
        null=True,
        blank=True,
        help_text="province",
    )
    city = models.CharField(
        max_length=50, verbose_name="city", null=True, blank=True, help_text="city"
    )
    district = models.CharField(
        max_length=50,
        verbose_name="district",
        null=True,
        blank=True,
        help_text="district",
    )
    isp = models.CharField(
        max_length=50, verbose_name="isp", null=True, blank=True, help_text="isp"
    )
    area_code = models.CharField(
        max_length=50,
        verbose_name="area_code",
        null=True,
        blank=True,
        help_text="area_code",
    )
    country_english = models.CharField(
        max_length=50,
        verbose_name="country_english",
        null=True,
        blank=True,
        help_text="country_english",
    )
    country_code = models.CharField(
        max_length=50,
        verbose_name="country_code",
        null=True,
        blank=True,
        help_text="country_code",
    )
    longitude = models.CharField(
        max_length=50,
        verbose_name="longitude",
        null=True,
        blank=True,
        help_text="longitude",
    )
    latitude = models.CharField(
        max_length=50,
        verbose_name="latitude",
        null=True,
        blank=True,
        help_text="latitude",
    )
    login_type = models.IntegerField(
        default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="type", help_text="type"
    )

    class Meta:
        db_table = table_prefix + "system_login_log"
        verbose_name = "operation table"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenter(CoreModel):
    title = models.CharField(max_length=100, verbose_name="title", help_text="title")
    content = models.TextField(verbose_name="content", help_text="content")
    target_type = models.IntegerField(
        default=0, verbose_name="target_type", help_text="target_type"
    )
    target_user = models.ManyToManyField(
        to=Users,
        related_name="user",
        through="MessageCenterTargetUser",
        through_fields=("messagecenter", "users"),
        blank=True,
        verbose_name="target_user",
        help_text="target_user",
    )
    target_dept = models.ManyToManyField(
        to=Dept,
        blank=True,
        db_constraint=False,
        verbose_name="target_dept",
        help_text="target_dept",
    )
    target_role = models.ManyToManyField(
        to=Role,
        blank=True,
        db_constraint=False,
        verbose_name="target_role",
        help_text="target_role",
    )

    class Meta:
        db_table = table_prefix + "message_center"
        verbose_name = "message center"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenterTargetUser(CoreModel):
    users = models.ForeignKey(
        Users,
        related_name="target_user",
        on_delete=models.CASCADE,
        db_constraint=False,
        verbose_name="users",
        help_text="users",
    )
    messagecenter = models.ForeignKey(
        MessageCenter,
        on_delete=models.CASCADE,
        db_constraint=False,
        verbose_name="message center",
        help_text="message center",
    )
    is_read = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="is_read",
        help_text="is_read",
    )

    class Meta:
        db_table = table_prefix + "message_center_target_user"
        verbose_name = "message center user table"
        verbose_name_plural = verbose_name
