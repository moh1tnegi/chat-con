from channels.generic.websocket import AsyncWebsocketConsumer
from . import models
import json

# import logging

# logging.basicConfig(filename='/home/mohit/Documents/git_repos/chat-con/debug.log',
#                     level=logging.DEBUG,
#                     filemode='w')
# logger = logging.getLogger()
# logger.debug('#logging asssssszzzzzzz!')


class ChatConsumer(AsyncWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(self)
        self.user_obj = ''

    async def connect(self):
        self.room_group_name = 'online_users'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        self.user_obj.is_online = False
        self.user_obj.save()
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'is_offline',
                'message': self.user_obj.username
            })

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name)

    async def receive(self, text_data):
        rec_msg = json.loads(text_data)
        try:
            usr_on = rec_msg['user_online']
            full_name = rec_msg['full_name']
            
            self.user_obj = models.User.objects.get(username__exact=usr_on)
            self.user_obj.is_online = True
            self.user_obj.save()

            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'is_online',
                    'message': usr_on,
                    'fulname': full_name
                })
        except KeyError:
            msg_frm = rec_msg['from']
            msg_to = rec_msg['to']
            msg_txt = rec_msg['text']

            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'text_msg',
                    'frm': msg_frm,
                    'to': msg_to,
                    'txt': msg_txt
                })

    async def is_online(self, event):
        usr = event['message']
        full_name = event['fulname']

        await self.send(text_data=json.dumps({
                'uname': usr,
                'full_name': full_name,
                'online': True
            }))

    async def is_offline(self, event):
        usr = event['message']

        await self.send(text_data=json.dumps({
                'uname': usr,
                'online': False
            }))

    async def text_msg(self, event):
        frm = event['frm']
        to = event['to']
        txt = event['txt']

        await self.send(text_data=json.dumps({
                'from': frm,
                'to': to,
                'txt_msg': txt
            }))