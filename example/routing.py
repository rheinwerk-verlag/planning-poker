from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import planning_poker.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(planning_poker.routing.websocket_urlpatterns)),
})
