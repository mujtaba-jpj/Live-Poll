from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/poll/<int:id>", consumers.PollConsumer.as_asgi()),
]
