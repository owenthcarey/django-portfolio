from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/image_gen/$", consumers.ImageGenConsumer.as_asgi()),
]
