import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DataConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        await self.accept()
        self.user = self.scope["user"]
        self.group_name = f"data-client"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print(self.group_name, self.channel_name)

        await self.send_json(
            {"type": "websocket.accept"}
        )

    async def receive_json(self, content):
        """
        Receive a message and broadcast it to connected clients.
        """
        """if self.scope["user"].is_anonymous:
            await self.close()
            return"""

        print(f"RECEIVED {content}")

        message = content["text"]

        response = {
                "type": "send.json",
                "text": message
            }

        print(f"RESPONDING: {response}")

        await self.channel_layer.group_send(
            self.group_name,
            response
        )

    async def disconnect(self, code):
        return await super().disconnect(code)