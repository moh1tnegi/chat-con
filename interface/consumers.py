from channels.generic.websocket import AsyncWebsocketConsumer
from . import models
import json

# import logging

# logging.basicConfig(filename='/home/mohit/Documents/git_repos/chat-con/log.txt',
#                     level=logging.DEBUG,
#                     filemode='w')
# logger = logging.getLogger()
# logger.debug('#logging asssssszzzzzzz!')


class ChatConsumer(AsyncWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(self)
        self.user_obj = ''

    async def connect(self):
        # logger.debug('000000000>>>>>>>>> connected')
        # self.room_name = 'online'
        self.room_group_name = 'online_users'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # logger.debug('000000000>>>>>>>>> diconnected')
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
        # logger.debug('000000000>>>>>>>>> received')
        user = json.loads(text_data)
        usr_on = user['user_online']
        
        self.user_obj = models.User.objects.get(username__exact=usr_on)
        self.user_obj.is_online = True
        self.user_obj.save()

        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'is_online',
                'message': usr_on
            })

    async def is_online(self, event):
        # logger.debug('000000000>>>>>>>>> is_online')
        usr = event['message']

        await self.send(text_data=json.dumps({
                'uname': usr,
                'online': True
            }))

    async def is_offline(self, event):
        usr = event['message']

        await self.send(text_data=json.dumps({
                'uname': usr,
                'online': False
            }))
