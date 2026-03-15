from django.contrib import admin

from users.models import UserModel, Follow

admin.site.register(UserModel)
admin.site.register(Follow)
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'notification_type', 'is_read', 'created_at')

    list_filter = ('notification_type', 'is_read', 'created_at')

    search_fields = ('sender__username', 'receiver__username')