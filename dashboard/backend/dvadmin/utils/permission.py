# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/6 006 10:30
@Remark: custom permission
"""
import re

from django.contrib.auth.models import AnonymousUser
from django.db.models import F
from rest_framework.permissions import BasePermission

from dvadmin.system.models import ApiWhiteList


def ValidationApi(reqApi, validApi):
    """
    Verify if the current user has interface permissions
    :param reqApi: current request
    :param validApi: valid api
    :return: True/False
    """
    if validApi is not None:
        valid_api = validApi.replace("{id}", ".*?")
        matchObj = re.match(valid_api, reqApi, re.M | re.I)
        if matchObj:
            return True
        else:
            return False
    else:
        return False


class AnonymousUserPermission(BasePermission):
    """ """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return True


def ReUUID(api):
    """
    replace uuid
    :param api:
    :return:
    """
    pattern = re.compile(r"[a-f\d]{4}(?:[a-f\d]{4}-){4}[a-f\d]{12}/$")
    m = pattern.search(api)
    if m:
        res = api.replace(m.group(0), ".*/")
        return res
    else:
        return None


class CustomPermission(BasePermission):
    """"""

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        #
        if request.user.is_superuser:
            return True
        else:
            api = request.path  #
            method = request.method
            methodList = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
            method = methodList.index(method)
            #
            api_white_list = ApiWhiteList.objects.values(
                permission__api=F("url"), permission__method=F("method")
            )
            api_white_list = [
                str(item.get("permission__api").replace("{id}", "([a-zA-Z0-9-]+)"))
                + ":"
                + str(item.get("permission__method"))
                + "$"
                for item in api_white_list
                if item.get("permission__api")
            ]
            # ********#
            if not hasattr(request.user, "role"):
                return False
            userApiList = request.user.role.values(
                "permission__api", "permission__method"
            )  # Obtain all interfaces owned by the current user's role
            ApiList = [
                str(item.get("permission__api").replace("{id}", "([a-zA-Z0-9-]+)"))
                + ":"
                + str(item.get("permission__method"))
                + "$"
                for item in userApiList
                if item.get("permission__api")
            ]
            new_api_ist = api_white_list + ApiList
            new_api = api + ":" + str(method)
            for item in new_api_ist:
                matchObj = re.match(item, new_api, re.M | re.I)
                if matchObj is None:
                    continue
                else:
                    return True
            else:
                return False
