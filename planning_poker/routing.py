from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'/(?P<poker_session>\w+)/$', consumers.PokerConsumer),
]
