# -*- coding: utf-8 -*-
import urllib

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    AsyncWebsocketConsumer,
)
import json

from channels.layers import get_channel_layer
from jwt import InvalidSignatureError

from application import settings

send_dict = {}


# message structure
def set_message(sender, msg_type, msg):
    text = {
        "sender": sender,
        "contentType": msg_type,
        "content": msg,
    }
    return text


@database_sync_to_async
def _get_message_center_instance(message_id):
    from dvadmin.system.models import MessageCenter

    _MessageCenter = MessageCenter.objects.filter(id=message_id).values_list(
        "target_user", flat=True
    )
    if _MessageCenter:
        return _MessageCenter
    else:
        return []


@database_sync_to_async
def _get_message_unread(user_id):
    from dvadmin.system.models import MessageCenterTargetUser

    count = MessageCenterTargetUser.objects.filter(users=user_id, is_read=False).count()
    return count or 0


def request_data(scope):
    query_string = scope.get("query_string", b"").decode("utf-8")
    qs = urllib.parse.parse_qs(query_string)
    return qs


class DvadminWebSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            import jwt

            self.service_uid = self.scope["url_route"]["kwargs"]["service_uid"]
            decoded_result = jwt.decode(
                self.service_uid, settings.SECRET_KEY, algorithms=["HS256"]
            )
            if decoded_result:
                self.user_id = decoded_result.get("user_id")
                self.chat_group_name = "user_" + str(self.user_id)
                # process when receive a connection，
                await self.channel_layer.group_add(
                    self.chat_group_name, self.channel_name
                )
                await self.accept()
                # send connection success
                await self.send_json(set_message("system", "SYSTEM", "connected"))
                # push message
                unread_count = await _get_message_unread(self.user_id)
                await self.send_json(
                    set_message(
                        "system",
                        "TEXT",
                        {"model": "message_center", "unread": unread_count},
                    )
                )
        except InvalidSignatureError:
            await self.disconnect(None)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)
        print("disconnect")
        await self.close(close_code)


class MegCenter(DvadminWebSocket):
    """
    message center
    """

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_id = text_data_json.get("message_id", None)
        user_list = await _get_message_center_instance(message_id)
        for send_user in user_list:
            await self.channel_layer.group_send(
                "user_" + str(send_user),
                {"type": "push.message", "json": text_data_json},
            )

    async def push_message(self, event):
        message = event["json"]
        await self.send(text_data=json.dumps(message))


def websocket_push(user_id, message):
    """
    push message
    """
    username = "user_" + str(user_id)
    print(103, message)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        username, {"type": "push.message", "json": message}
    )
