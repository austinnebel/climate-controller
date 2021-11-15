import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.dateparse import parse_datetime
from django.conf import settings

class DataConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        Called upon websocket connection.
        """

        await self.accept()
        self.user = self.scope["user"]
        self.group_name = f"data-client"

        # adds this channel to the data-client group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print(self.group_name, self.channel_name)

        return await self.send_json(
            {"type": "websocket.accept"}
        )

    async def receive_json(self, content):
        """
        Receives a JSON-like text object and sends it to all channels in the data-client group.
        This method is accessed by passing type: receive.json to the websocket.

        NOTE: Normally, content would be text, but AsyncJsonWebsocketConsumer does automatic conversions.

        Args:
            content (dict): JSON content to publish.
        """

        """if self.scope["user"].is_anonymous:
            await self.close()
            return"""

        print(f"RECEIVED {content}")

        message = content["text"]
        if "time" in message.keys():
            format = settings.REST_FRAMEWORK["DATETIME_FORMAT"]
            parsed = parse_datetime(message["time"])
            message["time"] = parsed.strftime(format)

        # type: send.json will cause group_send to call the inherited send_json method
        response = {
                "type": "send.json",
                "text": message
            }

        print(f"RESPONDING: {response}")

        return await self.channel_layer.group_send(
            self.group_name,
            response
        )

    async def disconnect(self, code):
        return await super().disconnect(code)