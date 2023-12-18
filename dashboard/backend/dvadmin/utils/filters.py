# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/6 006 12:39
@Remark: custom filter
"""
import operator
import re
from collections import OrderedDict
from functools import reduce

import six
from django.db.models import Q, F
from django.db.models.constants import LOOKUP_SEP
from django_filters import utils
from django_filters.filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.utils import get_model_field
from rest_framework.filters import BaseFilterBackend

from dvadmin.system.models import Dept, ApiWhiteList


def get_dept(dept_id: int, dept_all_list=None, dept_list=None):
    """
    Recursively obtain all subordinate departments of a department
    :param dept_id:
    :param dept_all_list:
    :param dept_list:
    :return:
    """
    if not dept_all_list:
        dept_all_list = Dept.objects.all().values("id", "parent")
    if dept_list is None:
        dept_list = [dept_id]
    for ele in dept_all_list:
        if ele.get("parent") == dept_id:
            dept_list.append(ele.get("id"))
            get_dept(ele.get("id"), dept_all_list, dept_list)
    return list(set(dept_list))


class DataLevelPermissionsFilter(BaseFilterBackend):
    """
    Data level permission filter
    0. Obtain the user's department ID. If there is no department, return empty
    1. Determine whether the filtered data has the "creator" field of the creator's department. If not, return all
    2. If the user does not have an associated role, return the data of this department
    3. Filter data based on the maximum permissions of roles (there may be multiple roles, and retrieve the maximum permissions)
    3.1 Determine whether the user is in the super administrator role/If there is 1 (all data), return all data

    4. Only for personal data permission, only return and filter personal data, and the department should be their own department
    (considering that users may change departments, only the department data of the current user can be viewed)
    5. Customize data permissions to obtain departments and filter based on departments

    """

    def filter_queryset(self, request, queryset, view):
        """ """
        api = request.path  #
        method = request.method  #
        methodList = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        method = methodList.index(method)

        api_white_list = ApiWhiteList.objects.filter(enable_datasource=False).values(
            permission__api=F("url"), permission__method=F("method")
        )
        api_white_list = [
            str(item.get("permission__api").replace("{id}", ".*?"))
            + ":"
            + str(item.get("permission__method"))
            for item in api_white_list
            if item.get("permission__api")
        ]
        for item in api_white_list:
            new_api = api + ":" + str(method)
            matchObj = re.match(item, new_api, re.M | re.I)
            if matchObj is None:
                continue
            else:
                return queryset

        if request.user.is_superuser == 0:
            # 0. Obtain the user's department ID. If there is no department, return empty
            user_dept_id = getattr(request.user, "dept_id", None)
            if not user_dept_id:
                return queryset.none()

            # 1. Determine if the filtered data has the "dept_belong_id" field in the department where the creator belongs
            if not getattr(queryset.model, "dept_belong_id", None):
                return queryset

            # 2. If the user does not have an associated role, return the data of this department
            if not hasattr(request.user, "role"):
                return queryset.filter(dept_belong_id=user_dept_id)

            # 3. Obtain all permission ranges based on all roles
            # (0, "Only personal data permission"),
            # (1, "Data permissions for this department and below"),
            # (2, "Data permissions of this department"),
            # (3, "All data permissions"),
            # (4, "custom data permissions")
            role_list = request.user.role.filter(status=1).values("admin", "data_range")
            dataScope_list = []  #
            for ele in role_list:
                # Determine if the user is in the super administrator role/If they have [All Data Permissions], return all data
                if 3 == ele.get("data_range") or ele.get("admin"):
                    return queryset
                dataScope_list.append(ele.get("data_range"))
            dataScope_list = list(set(dataScope_list))

            # 4. Only for personal data permission, only return and filter personal data,
            # and the department is the own department (considering that users may change departments,
            # only the department data of the current user can be viewed)
            if 0 in dataScope_list:
                return queryset.filter(
                    creator=request.user, dept_belong_id=user_dept_id
                )

            # 5.Customize data permissions to obtain departments and filter based on departments
            dept_list = []
            for ele in dataScope_list:
                if ele == 4:
                    dept_list.extend(
                        request.user.role.filter(status=1).values_list(
                            "dept__id", flat=True
                        )
                    )
                elif ele == 2:
                    dept_list.append(user_dept_id)
                elif ele == 1:
                    dept_list.append(user_dept_id)
                    dept_list.extend(
                        get_dept(
                            user_dept_id,
                        )
                    )
            if queryset.model._meta.model_name == "dept":
                return queryset.filter(id__in=list(set(dept_list)))
            return queryset.filter(dept_belong_id__in=list(set(dept_list)))
        else:
            return queryset


class CustomDjangoFilterBackend(DjangoFilterBackend):
    lookup_prefixes = {
        "^": "istartswith",
        "=": "iexact",
        "@": "search",
        "$": "iregex",
        "~": "icontains",
    }

    def construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = "icontains"
        return LOOKUP_SEP.join([field_name, lookup])

    def find_filter_lookups(self, orm_lookups, search_term_key):
        for lookup in orm_lookups:
            # if lookup.find(search_term_key) >= 0:
            new_lookup = lookup.split("__")[0]
            #
            if new_lookup == search_term_key:
                return lookup
        return None

    def get_filterset_class(self, view, queryset=None):
        """
        Return the `FilterSet` class used to filter the queryset.
        """
        filterset_class = getattr(view, "filterset_class", None)
        filterset_fields = getattr(view, "filterset_fields", None)

        # TODO: remove assertion in 2.1
        if filterset_class is None and hasattr(view, "filter_class"):
            utils.deprecate(
                "`%s.filter_class` attribute should be renamed `filterset_class`."
                % view.__class__.__name__
            )
            filterset_class = getattr(view, "filter_class", None)

        # TODO: remove assertion in 2.1
        if filterset_fields is None and hasattr(view, "filter_fields"):
            utils.deprecate(
                "`%s.filter_fields` attribute should be renamed `filterset_fields`."
                % view.__class__.__name__
            )
            filterset_fields = getattr(view, "filter_fields", None)

        if filterset_class:
            filterset_model = filterset_class._meta.model

            # FilterSets do not need to specify a Meta class
            if filterset_model and queryset is not None:
                assert issubclass(
                    queryset.model, filterset_model
                ), "FilterSet model %s does not match queryset model %s" % (
                    filterset_model,
                    queryset.model,
                )

            return filterset_class

        if filterset_fields and queryset is not None:
            MetaBase = getattr(self.filterset_base, "Meta", object)

            class AutoFilterSet(self.filterset_base):
                @classmethod
                def get_filters(cls):
                    """
                    Get all filters for the filterset. This is the combination of declared and
                    generated filters.
                    """

                    # No model specified - skip filter generation
                    if not cls._meta.model:
                        return cls.declared_filters.copy()

                    # Determine the filters that should be included on the filterset.
                    filters = OrderedDict()
                    fields = cls.get_fields()
                    undefined = []

                    for field_name, lookups in fields.items():
                        field = get_model_field(cls._meta.model, field_name)
                        from django.db import models
                        from timezone_field import TimeZoneField

                        #
                        if isinstance(field, (models.JSONField, TimeZoneField)):
                            continue
                        # warn if the field doesn't exist.
                        if field is None:
                            undefined.append(field_name)

                        for lookup_expr in lookups:
                            filter_name = cls.get_filter_name(field_name, lookup_expr)

                            # If the filter is explicitly declared on the class, skip generation
                            if filter_name in cls.declared_filters:
                                filters[filter_name] = cls.declared_filters[filter_name]
                                continue

                            if field is not None:
                                filters[filter_name] = cls.filter_for_field(
                                    field, field_name, lookup_expr
                                )

                    # Allow Meta.fields to contain declared filters *only* when a list/tuple
                    if isinstance(cls._meta.fields, (list, tuple)):
                        undefined = [
                            f for f in undefined if f not in cls.declared_filters
                        ]

                    if undefined:
                        raise TypeError(
                            "'Meta.fields' must not contain non-model field names: %s"
                            % ", ".join(undefined)
                        )

                    # Add in declared filters. This is necessary since we don't enforce adding
                    # declared filters to the 'Meta.fields' option
                    filters.update(cls.declared_filters)
                    return filters

                class Meta(MetaBase):
                    model = queryset.model
                    fields = filterset_fields

            return AutoFilterSet

        return None

    def filter_queryset(self, request, queryset, view):
        filterset = self.get_filterset(request, queryset, view)
        if filterset is None:
            return queryset
        if filterset.__class__.__name__ == "AutoFilterSet":
            queryset = filterset.queryset
            orm_lookups = []
            for search_field in filterset.filters:
                if isinstance(filterset.filters[search_field], CharFilter):
                    orm_lookups.append(
                        self.construct_search(six.text_type(search_field))
                    )
                else:
                    orm_lookups.append(search_field)
            conditions = []
            queries = []
            for search_term_key in filterset.data.keys():
                orm_lookup = self.find_filter_lookups(orm_lookups, search_term_key)
                if not orm_lookup:
                    continue
                query = Q(**{orm_lookup: filterset.data[search_term_key]})
                queries.append(query)
            if len(queries) > 0:
                conditions.append(reduce(operator.and_, queries))
                queryset = queryset.filter(reduce(operator.and_, conditions))
                return queryset
            else:
                return queryset

        if not filterset.is_valid() and self.raise_exception:
            raise utils.translate_validation(filterset.errors)
        return filterset.qs
