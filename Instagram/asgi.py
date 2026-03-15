import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import direct.routing # Импорт твоего роутинга из приложения direct

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Instagram.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            direct.routing.websocket_urlpatterns
        )
    ),
})