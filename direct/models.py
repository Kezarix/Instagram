from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Dialog(models.Model):
    users = models.ManyToManyField(User, related_name='dialogs')
    updated_at = models.DateTimeField(auto_now=True)

    def other_user(self, me):
        return self.users.exclude(id=me.id).first()


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='dm/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)