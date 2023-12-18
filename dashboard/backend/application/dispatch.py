#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import connection


def is_tenants_mode():
    """
    tenant mode
    :return: True/False
    """
    return hasattr(connection, "tenant") and connection.tenant.schema_name


# ================================================= #
# ******************** initialize ***************** #
# ================================================= #
def _get_all_dictionary():
    from dvadmin.system.models import Dictionary

    queryset = Dictionary.objects.filter(status=True, is_value=False)
    data = []
    for instance in queryset:
        data.append(
            {
                "id": instance.id,
                "value": instance.value,
                "children": list(
                    Dictionary.objects.filter(parent=instance.id)
                    .filter(status=1)
                    .values("label", "value", "type", "color")
                ),
            }
        )
    return {ele.get("value"): ele for ele in data}


def _get_all_system_config():
    data = {}
    from dvadmin.system.models import SystemConfig

    system_config_obj = (
        SystemConfig.objects.filter(parent_id__isnull=False)
        .values("parent__key", "key", "value", "form_item_type")
        .order_by("sort")
    )
    for system_config in system_config_obj:
        value = system_config.get("value", "")
        if value and system_config.get("form_item_type") == 7:
            value = value[0].get("url")
        data[f"{system_config.get('parent__key')}.{system_config.get('key')}"] = value
    return data


def init_dictionary():
    """
    initialize dictionary information
    :return:
    """
    try:
        if is_tenants_mode():
            from django_tenants.utils import tenant_context, get_tenant_model

            for tenant in get_tenant_model().objects.filter():
                with tenant_context(tenant):
                    settings.DICTIONARY_CONFIG[
                        connection.tenant.schema_name
                    ] = _get_all_dictionary()
        else:
            settings.DICTIONARY_CONFIG = _get_all_dictionary()
    except Exception:
        print("Please perform database migration first")
    return


def init_system_config():
    """
    initialize system information
    :param name:
    :return:
    """
    try:
        if is_tenants_mode():
            from django_tenants.utils import tenant_context, get_tenant_model

            for tenant in get_tenant_model().objects.filter():
                with tenant_context(tenant):
                    settings.SYSTEM_CONFIG[
                        connection.tenant.schema_name
                    ] = _get_all_system_config()
        else:
            settings.SYSTEM_CONFIG = _get_all_system_config()
    except Exception:
        print("Please perform database migration first")
    return


def refresh_dictionary():
    """
    refresh dictionary information
    :return:
    """
    if is_tenants_mode():
        from django_tenants.utils import tenant_context, get_tenant_model

        for tenant in get_tenant_model().objects.filter():
            with tenant_context(tenant):
                settings.DICTIONARY_CONFIG[
                    connection.tenant.schema_name
                ] = _get_all_dictionary()
    else:
        settings.DICTIONARY_CONFIG = _get_all_dictionary()


def refresh_system_config():
    """
    refresh system config
    :return:
    """
    if is_tenants_mode():
        from django_tenants.utils import tenant_context, get_tenant_model

        for tenant in get_tenant_model().objects.filter():
            with tenant_context(tenant):
                settings.SYSTEM_CONFIG[
                    connection.tenant.schema_name
                ] = _get_all_system_config()
    else:
        settings.SYSTEM_CONFIG = _get_all_system_config()


# ================================================= #
# **************** dictionary config*************** #
# ================================================= #
def get_dictionary_config(schema_name=None):
    """
    get all dictionary config
    :param schema_name: the schema_name corresponding to the dictionary configuration
    :return:
    """
    if not settings.DICTIONARY_CONFIG:
        refresh_dictionary()
    if is_tenants_mode():
        dictionary_config = settings.DICTIONARY_CONFIG[
            schema_name or connection.tenant.schema_name
        ]
    else:
        dictionary_config = settings.DICTIONARY_CONFIG
    return dictionary_config or {}


def get_dictionary_values(key, schema_name=None):
    """
    get dictionary values
    :param key: the key (dictionary number) corresponding to the dictionary configuration
    :param schema_name: the schema_name corresponding to the dictionary configuration
    :return:
    """
    dictionary_config = get_dictionary_config(schema_name)
    return dictionary_config.get(key)


def get_dictionary_label(key, name, schema_name=None):
    """
    get dictionary labels
    :param key: the key (dictionary number) corresponding to the dictionary configuration
    :param name: the value corresponding to the dictionary configuration
    :param schema_name: the schema_name corresponding to the dictionary configuration
    :return:
    """
    children = get_dictionary_values(key, schema_name) or []
    for ele in children:
        if ele.get("value") == str(name):
            return ele.get("label")
    return ""


# ================================================= #
# ***************** system config ***************** #
# ================================================= #
def get_system_config(schema_name=None):
    """
    get all system config
    1.parent_key, return all child，{ "parent_key.child_key" : "value" }
    2."parent_key.child_key"，return child value
    :param schema_name: the schema_name corresponding to the dictionary configuration
    :return:
    """
    if not settings.SYSTEM_CONFIG:
        refresh_system_config()
    if is_tenants_mode():
        dictionary_config = settings.SYSTEM_CONFIG[
            schema_name or connection.tenant.schema_name
        ]
    else:
        dictionary_config = settings.SYSTEM_CONFIG
    return dictionary_config or {}


def get_system_config_values(key, schema_name=None):
    """
    get system config values
    :param key: the key (dictionary number) corresponding to the dictionary configuration
    :param schema_name: the schema_name corresponding to the dictionary configuration
    :return:
    """
    system_config = get_system_config(schema_name)
    return system_config.get(key)


def get_system_config_label(key, name, schema_name=None):
    """
    get system config labels
    :param key: the key (dictionary number) corresponding to the dictionary configuration
    :param name: the value corresponding to the dictionary configuration
    :param schema_name: the schema_name corresponding to the dictionary configuration
    :return:
    """
    children = get_system_config_values(key, schema_name) or []
    for ele in children:
        if ele.get("value") == str(name):
            return ele.get("label")
    return ""
