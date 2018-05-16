from .consumers import *
from django.conf.urls import url

ws_urlpatterns = [
	url(r'^contact_us/$', here),
]