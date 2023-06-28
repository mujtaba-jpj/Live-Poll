from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/btc/", consumers.GraphConsumer.as_asgi()),
]
