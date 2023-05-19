from channels.routing import ProtocolTypeRouter, URLRouter
import image_gen.routing
from django_portfolio import asgi

application = ProtocolTypeRouter(
    {
        "http": asgi.application,
        "websocket": URLRouter(image_gen.routing.websocket_urlpatterns),
    }
)
