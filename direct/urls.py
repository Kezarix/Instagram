from django.urls import path
from . import views

app_name = 'direct'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:dialog_id>/', views.dialog, name='dialog'),
    path('<int:user_id>/start/', views.start_dialog, name='start'),
    path('api/my-chats/', views.my_chats_api, name='my_chats_api'),
]
