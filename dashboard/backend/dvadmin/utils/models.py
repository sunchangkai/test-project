# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/5/31 031 22:08
@Remark: Common Foundation Model Class
"""
import uuid

from django.apps import apps
from django.db import models
from django.db.models import QuerySet

from application import settings

table_prefix = settings.TABLE_PREFIX  #


class SoftDeleteQuerySet(QuerySet):
    pass


class SoftDeleteManager(models.Manager):
    """"""

    def __init__(self, *args, **kwargs):
        self.__add_is_del_filter = False
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        #
        if not kwargs.get("is_deleted") is None:
            self.__add_is_del_filter = True
        return super(SoftDeleteManager, self).filter(*args, **kwargs)

    def get_queryset(self):
        if self.__add_is_del_filter:
            return SoftDeleteQuerySet(self.model, using=self._db).exclude(
                is_deleted=False
            )
        return SoftDeleteQuerySet(self.model).exclude(is_deleted=True)

    def get_by_natural_key(self, name):
        return SoftDeleteQuerySet(self.model).get(username=name)


class SoftDeleteModel(models.Model):
    """
    Once inherited, soft delete will be enabled
    """

    is_deleted = models.BooleanField(
        verbose_name="is_deleted", help_text="is_deleted", default=False, db_index=True
    )
    objects = SoftDeleteManager()

    class Meta:
        abstract = True
        verbose_name = "soft delete model"
        verbose_name_plural = verbose_name

    def delete(self, using=None, soft_delete=True, *args, **kwargs):
        """ """
        self.is_deleted = True
        self.save(using=using)


class CoreModel(models.Model):
    """
    The core standard abstract model model can be directly inherited and used

    When adding fields and overwriting fields, do not modify the field names, they must be unify
    """

    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    description = models.CharField(
        max_length=255,
        verbose_name="description",
        null=True,
        blank=True,
        help_text="description",
    )
    creator = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_query_name="creator_query",
        null=True,
        verbose_name="creator",
        help_text="creator",
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    modifier = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="modifier",
        verbose_name="modifier",
    )
    dept_belong_id = models.CharField(
        max_length=255,
        help_text="dept_belong_id",
        null=True,
        blank=True,
        verbose_name="dept_belong_id",
    )
    update_datetime = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        help_text="update_datetime",
        verbose_name="update_datetime",
    )
    create_datetime = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="create_datetime",
        verbose_name="create_datetime",
    )

    class Meta:
        abstract = True
        verbose_name = "core model"
        verbose_name_plural = verbose_name


def get_all_models_objects(model_name=None):
    """
    :return: {}
    """
    settings.ALL_MODELS_OBJECTS = {}
    if not settings.ALL_MODELS_OBJECTS:
        all_models = apps.get_models()
        for item in list(all_models):
            table = {
                "tableName": item._meta.verbose_name,
                "table": item.__name__,
                "tableFields": [],
            }
            for field in item._meta.fields:
                fields = {"title": field.verbose_name, "field": field.name}
                table["tableFields"].append(fields)
            settings.ALL_MODELS_OBJECTS.setdefault(
                item.__name__, {"table": table, "object": item}
            )
    if model_name:
        return settings.ALL_MODELS_OBJECTS[model_name] or {}
    return settings.ALL_MODELS_OBJECTS or {}
