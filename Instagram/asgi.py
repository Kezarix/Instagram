import os
import django
from django.core.asgi import get_asgi_application

# 1. Сначала устанавливаем настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Instagram.settings')

# 2. Инициализируем Django
django.setup()

# 3. ТОЛЬКО ТЕПЕРЬ импортируем всё остальное
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import direct.routing  # Теперь этот импорт не вызовет ошибку

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            direct.routing.websocket_urlpatterns
        )
    ),
})