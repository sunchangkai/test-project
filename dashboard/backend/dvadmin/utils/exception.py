# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/2 002 16:06
@Remark: custom exception handler
"""
import logging
import traceback

from django.db.models import ProtectedError
from rest_framework.exceptions import (
    APIException as DRFAPIException,
    AuthenticationFailed,
)
from rest_framework.views import set_rollback

from dvadmin.utils.json_response import ErrorResponse

logger = logging.getLogger(__name__)


def CustomExceptionHandler(ex, context):
    """

    Purpose: (1) Cancel all 500 abnormal responses and return a unified response as a standard error
             (2) Accurately display error information
    :param ex:
    :param context:
    :return:
    """
    msg = ""
    code = 4000

    if isinstance(ex, AuthenticationFailed):
        code = 401
        msg = ex.detail
    elif isinstance(ex, DRFAPIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, ProtectedError):
        set_rollback()
        msg = "delete failed: this data is bound to other data"
    # elif isinstance(ex, DatabaseError):
    #     set_rollback()
    #     msg = "The interface is abnormal. Please contact the administrator"
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        msg = str(ex)

    # errorMsg = msg
    # for key in errorMsg:
    #     msg = errorMsg[key][0]

    return ErrorResponse(msg=msg, code=code)
