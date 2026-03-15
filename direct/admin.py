from django.contrib import admin
from .models import Dialog, Message


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_users', 'updated_at')

    def display_users(self, obj):
        return ", ".join([u.username for u in obj.users.all()])

    display_users.short_description = 'Участники'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'dialog', 'text', 'created_at')
    list_filter = ('created_at', 'sender')
    search_fields = ('text',)