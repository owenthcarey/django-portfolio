import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


class ImageGenConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        """This method is called when the WebSocket is handshaking as part of the connection process."""
        print("Connecting...")
        await self.accept()  # Accepts the WebSocket connection.
        print("Connected.")

    async def disconnect(self, close_code: int) -> None:
        """This method is called when the WebSocket closes for any reason."""
        print(f"Disconnected with close code {close_code}")

    async def receive(self, text_data: str) -> None:
        """
        This method is called when the server receives a message.

        Args:
            text_data: The text data sent from the client side.
        """
        print("Received data: ", text_data)
        text_data_json: dict = json.loads(text_data)  # Parsing the JSON data from the client
        prompt: str = text_data_json["prompt"]
        print("Prompt: ", prompt)

        for i in range(50):
            progress: int = (i + 1) * 2  # Here, calculate the progress
            print("Progress: ", progress)

            # Pause for a second
            await asyncio.sleep(1)

            # Sending a message back to the client with the image data and the progress
            await self.send(
                text_data=json.dumps(
                    {
                        "image": "dummy_image_data",  # Dummy image data for now
                        "progress": progress,  # The progress of the image generation
                    }
                )
            )
        print("Data sent.")
