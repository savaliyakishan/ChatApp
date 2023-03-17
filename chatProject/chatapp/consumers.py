from channels.generic.websocket import AsyncJsonWebsocketConsumer,WebsocketConsumer
from channels.db import DatabaseSyncToAsync
from asgiref.sync import sync_to_async,async_to_sync
from .models import *
import json


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


class CallConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

        # response to client, that we are connected.
        self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.my_name,
            self.channel_name
        )

    # Receive message from client WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json['type']

        if eventType == 'login':
            name = text_data_json['data']['name']

            # we will use this as room name as well
            self.my_name = name

            # Join room
            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )
        
        if eventType == 'call':
            name = text_data_json['data']['name']


            # to notify the callee we sent an event to the group name
            # and their's groun name is the name
            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'answer_call':
            # has received call from someone now notify the calling user
            # we can notify to the group with the caller name
            
            caller = text_data_json['data']['caller']
            # print(self.my_name, "is answering", caller, "calls.")

            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'ICEcandidate':

            user = text_data_json['data']['user']
            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

    def call_received(self, event):

        # print(event)
        self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))


    def call_answered(self, event):

        # print(event)
        print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data']
        }))


    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({
            'type': 'ICEcandidate',
            'data': event['data']
        }))