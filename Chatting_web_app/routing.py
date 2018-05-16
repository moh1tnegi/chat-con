from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import interface.routing

asgi_apps = ProtocolTypeRouter({
				'websocket': AuthMiddlewareStack(
					URLRouter(interface.routing.ws_urlpatterns)
				)
			})