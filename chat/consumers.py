from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import sync_to_async, async_to_sync
import channels
import json
import os
import aioredis
import asyncio


class ChatRoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @database_sync_to_async
    def create_msg(self, user_id=None, message=None, room=None):
        if user_id is not None:
            sender = User.objects.get(id=user_id)
            msg = Message.objects.create(
                author=sender, message=message, room_name=room)
            msg.save()
            return msg
        else:
            get_msgs = Message.objects.filter(room_name__in=[room])
            serializer = MessageSerializer(get_msgs, many=True)

            return serializer.data

    async def connect(self):
        # init redis connection
        self.redis = await aioredis.create_redis(os.environ.get('REDIS_URL', 'redis://localhost:6379'))

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.messages = await self.create_msg(room=self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'db_messages': self.messages,
        }))

    async def disconnect(self, close_code):
        # close redis connection
        self.redis.close()
        await self.redis.wait_closed()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        username = text_data_json['username']
        user_id = text_data_json['user_id']

        if type == 'chatroom_message':
            self.msg = await self.create_msg(user_id, message, self.room_name)

        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': type,
                'message': message,
                'username': username,
                'user_id': user_id
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    async def get_user(self, event):
        # print(event['message'])
        if event['message'] == 'disconnect':
            try:
                # remove user
                await self.redis.hdel(self.room_name, event['username'])
            except ValueError:
                print('user already removed')
        else:
            # add current user in chat
            await self.redis.hmset(self.room_name, event['username'], event['username'])

        users_dict = await self.redis.hgetall(self.room_name)

        # convert dict to list
        users_dict_values = list(users_dict.values())
        users_list = []
        for i in range(len(users_dict_values)):
            users_list.append(users_dict_values[i].decode('UTF-8'))

        print(f'current users: {users_list}')
        await self.send(text_data=json.dumps({
            'users': users_list
        }))
