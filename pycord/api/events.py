from ..utils import json
from collections import deque
from ..models import Message
from ..models import ClientUser, Guild, Message

class EventHandler:
    def __init__(self, shard):
        self.shard = shard
        self.client = shard.client
        self.api = self.client.api
        self.emitted_ready = False

    async def handle_ready(self, data):
        self.client.user = ClientUser(self.client, data)
        for guild in data['guilds']:
            self.client.guilds.add(Guild(self.client, guild))

    async def handle_message_create(self, data):
        message = Message(self.client, data)
        self.client.messages.add(message)
        await self.client.emit('message', message)

    async def handle_guild_create(self, data):
        guild = self.client.guilds.get(int(data['id']))
        if guild:
            guild.from_dict(data)
        else:
            self.client.guilds.add(Guild(self.client, data))

        if not self.emitted_ready:
            if len([None for g in self.client.guilds if g.unavailable]) == 0:
                await self.client.emit('ready')
                self.emitted_ready = True
