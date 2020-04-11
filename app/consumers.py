import asyncio

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
import json

from django.db.models import Sum

from .models import Stream, PollStat, LikeDislike
from .utils import *


def get_current_stream():
    return Stream.objects.get(active=True)


def get_current_stream_id():
    return get_current_stream().stream_id


def is_stream_active():
    return Stream.objects.filter(active=True).exists()


class Handler:
    # Do not touch this methods, they should be empty
    async def send(self, command, pack):
        pass

    async def send_broadcast(self, command, pack):
        pass

    async def send_broadcast_but_me(self, command, pack):
        pass


class PollHandler(Handler):
    name = "poll"

    @action(command="like")
    async def like(self, sender, packet):
        await sync_to_async(self.vote)(sender, True)
        await self.update(sender)
        print("like")

    @action(command="dislike")
    async def dislike(self, sender, packet):
        await sync_to_async(self.vote)(sender, False)
        await self.update(sender)
        print("dislike")

    @staticmethod
    def get_stat(sender):
        stream = get_current_stream()
        stat = PollStat.objects.filter(stream=stream)
        likes, dises = 0, 0
        for s in stat:
            if s.vote == LikeDislike.LIKE:
                likes += 1
            else:
                dises += 1
        print(likes, dises)
        return likes, dises

    async def update(self, sender):
        likes, dislikes = await sync_to_async(PollHandler.get_stat)(sender)
        await self.send_broadcast("update", {"likes": likes, "dislikes": dislikes})

    @staticmethod
    def vote(sender, like):
        PollStat(user=sender.scope["user"], stream=get_current_stream(),
                 vote=LikeDislike.LIKE if like else LikeDislike.DISLIKE).save()


class QueueHandler(Handler):
    name = "queue"

    async def broadcast_current_stream(self, sender):
        await self.send_broadcast_but_me('set_stream', {"stream": await sync_to_async(get_current_stream_id)()})

    @action(command="queue")
    async def queue(self, sender, packet):
        print('queueing')
        user = sender.scope["user"]
        if user.is_anonymous:
            await self.send('error', {"error": "You should be authorized to start stream"})
            print('not logged')
            return
        is_streaming = await sync_to_async(is_stream_active)()
        print(is_streaming)
        if is_streaming:
            print('someone streaming')
            # sender.send_json({"error": "Someone is streaming right now"})
            # return
            stream = await sync_to_async(get_current_stream)()
            stream.active = False
            await sync_to_async(stream.save)()
        model = Stream(publisher=user, stream_id=packet['id'])
        await sync_to_async(model.save)()
        print(user.username)
        await self.broadcast_current_stream(sender)
        print('save')
        #await asyncio.sleep(40)
        #model.active = False
        #await sync_to_async(model.save)()
        #print('end')


class ChatHandler(Handler):
    name = 'chat'

    @action(command='send_message')
    async def send_message(self, sender, packet):
        print('sending message packet', packet)
        print('sending message sender', sender)
        await self.send_broadcast('send_message', {
            'message': packet['message'],
            'nickname': packet['nickname']
        })


class WSConsumer(AsyncJsonWebsocketConsumer):
    GROUP_NAME = 'main'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handlers = [
            PollHandler(self),
            QueueHandler(self),
            ChatHandler(self)
        ]

        self.handlers = {h.name: h for h in self.handlers}

    async def send_broadcast(self, handler, command, data, name=None):
        print("broadcast", handler, command, data, name)
        await self.channel_layer.group_send(self.GROUP_NAME, {
            "type": "send.command", "handler": handler, "command": command, "data": data, "chan_name": name
        })

    async def send_internal_broadcast_message(self, handler, command, data):
        print("Sending internal event {}".format(command))
        await self.channel_layer.group_send(self.GROUP_NAME, {
            "type": "send.internal", "handler": handler, "command": command, "data": data
        })

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        for _, h in self.handlers.items():
            await h.connection_opened(self.scope['user'] if 'user' in self.scope else None)
        print("connected", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)
        print("Disconnected")

    async def receive_json(self, content, **kwargs):
        print("Received: {}".format(content))
        handler, packet_name = content['handler'], content['message']
        await find_action(self.handlers[handler], packet_name)(self, content['data'] if 'data' in content else None)

    async def send_packet(self, handler, command, data):
        await self.send_json({"handler": handler, "command": command, "data": data})

    async def send_command(self, event):
        if not event['chan_name'] or self.channel_name != event['chan_name']:
            await self.send_packet(event["handler"], event["command"], event["data"])

    async def send_internal(self, event):
        print("Received internal event {}".format(event))
        print(find_action(self.handlers[event['handler']], event['command'], True))
        await find_action(self.handlers[event['handler']], event['command'], True)(self, event['data'] if 'data' in event else None)
