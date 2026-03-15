from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.main_view, name='main_view'),

    # Создание поста
    path('create-post/', views.create_post_view, name='create_post'),

    path('explore/', views.explore, name='explore'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path("reels/", views.reels_page, name="reels"),

    # Комментарии и лайки
    path('post/<int:pk>/comment/', views.create_comment, name='create_comment'),
    path('post/<int:pk>/like/', views.toggle_post_like, name='toggle_like'),

    path('comment/<int:pk>/like/', views.toggle_comment_like, name='toggle_comment_like'),
    path('comment/<int:pk>/reply/', views.reply_comment, name='reply_comment'),

    path('reply/<int:pk>/like/', views.toggle_reply_like, name='toggle_reply_like'),

    path('notifications/', views.notifications_view, name='notifications'),
]
