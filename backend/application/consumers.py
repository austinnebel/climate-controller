import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.dateparse import parse_datetime
from django.conf import settings

CLIENT_GROUP = "client-group"
EMBEDDED_GROUP = "embedded-group"

class ClientWebsocketConsumer(AsyncJsonWebsocketConsumer):
    """
    This class is used to broadcast climate data to clients.
    Once a client connects to this consumer they will receive all
    messages broadcasted by `EmbeddedWebsocketConsumer`
    """

    async def connect(self):
        """
        Called upon websocket connection. This accepts the request,
        adds the new channel to a group in the channel layer (redis),
        and replies to the request.
        """

        await self.accept()
        self.user = self.scope["user"]
        self.group_name = CLIENT_GROUP

        # adds this channel to the `CLIENT_GROUP` group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("Added channel to", self.group_name)

        return await self.send_json(
            {"type": "websocket.accept"}
        )

    async def disconnect(self, code):
        """
        Disconnects from the websocket connection.
        """
        return await super().disconnect(code)


class EmbeddedWebsocketConsumer(AsyncJsonWebsocketConsumer):
    """
    This class is used to consume websocket connections. It runs asynchronously
    and sends each received message to all connected clients.
    """

    async def connect(self):
        """
        Called upon websocket connection. This accepts the request,
        adds the new channel to a group in the channel layer (redis),
        and replies to the request.
        """

        await self.accept()
        self.user = self.scope["user"]
        self.group_name = EMBEDDED_GROUP

        # adds this channel to the `EMBEDDED_GROUP` group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("Added channel to", self.group_name)

        return await self.send_json(
            {"type": "websocket.accept"}
        )

    async def receive_json(self, content):
        """
        Receives a JSON-like text object and sends it to all channels in `CLIENT_GROUP`.
        This method is accessed by passing type: receive.json to the websocket.

        NOTE: Normally, content would be text, but AsyncJsonWebsocketConsumer does automatic conversions.

        Args:
            content (dict): JSON content to publish.
        """

        """if self.scope["user"].is_anonymous:
            await self.close()
            return"""

        # print(f"RECEIVED {content}")

        message = content["text"]
        if "time" in message.keys():
            format = settings.REST_FRAMEWORK["DATETIME_FORMAT"]
            parsed = parse_datetime(message["time"])
            message["time"] = parsed.strftime(format)

        # `"type": "send.json"` will cause `group_send` to call the `send_json` method
        # inherited from `AsyncJsonWebsocketConsumer`
        response = {
                "type": "send.json",
                "text": message
            }

        print(f"Broadcasting to clients: {response}")

        # Broadcast received message to all channels in `CLIENT_GROUP`
        return await self.channel_layer.group_send(
            CLIENT_GROUP,
            response
        )

    async def disconnect(self, code):
        """
        Disconnects from the websocket connection.
        """
        return await super().disconnect(code)