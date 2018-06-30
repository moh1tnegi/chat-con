from . import consumers
from django.conf.urls import url

ws_urlpatterns = [
    url(r'^$', consumers.ChatConsumer),
]
