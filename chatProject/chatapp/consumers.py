from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import DatabaseSyncToAsync
from asgiref.sync import sync_to_async
from .models import *


class myAsyncJsonConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        sender = self.scope['url_route']['kwargs']['sender_id']
        reciver = self.scope['url_route']['kwargs']['reciver_id']
        self.groupname = f'user_chatroom_{sender}_{reciver}'
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add(
                self.groupname,
                self.channel_name
            )
            await self.accept()
        else:
            self.close()

    async def receive_json(self, content, **kwargs):
        sender = self.scope['url_route']['kwargs']['sender_id']
        reciver = self.scope['url_route']['kwargs']['reciver_id']
        self.groupname = f'user_chatroom_{sender}_{reciver}'
        self.reciver_obj = await DatabaseSyncToAsync(User.objects.get)(id=reciver)
        if self.scope['user'].is_authenticated:
            self.message = await DatabaseSyncToAsync(messageInfo.objects.create)(
                senderUserInfo = content['sender_user_id'],
                reciveUserInfo = self.reciver_obj,
                message = content['message']
            )
            self.reciver_groupname = f'user_chatroom_{reciver}_{sender}'
            response = {
                "message":content["message"],
                "sender_group_name":self.groupname,
                "reciver_group_name":self.reciver_groupname,
            }

            await self.channel_layer.group_send(
                self.groupname,
                {
                    "type": "groupchat.message",
                    "message": response
                }
            )

            await self.channel_layer.group_send(
                self.reciver_groupname,
                {
                    "type": "reciver_groupchat.message",
                    "message": response
                }
            )

    async def reciver_groupchat_message(self, event):
            await self.send_json({"message": event['message']})  

    async def groupchat_message(self, event):
        await self.send_json({"message": event['message']})    

    async def disconnect(self, code):
        sender = self.scope['url_route']['kwargs']['sender_id']
        reciver = self.scope['url_route']['kwargs']['reciver_id']
        self.groupname = f'user_chatroom_{sender}_{reciver}'
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        await self.close()
