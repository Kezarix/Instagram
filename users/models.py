from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserModel(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True, blank=True,
        verbose_name=_('avatar'),
    )
    bio = models.TextField(blank=True, verbose_name=_('bio'))
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.username

    @property
    def unread_notifications_count(self):
        return self.notifications.filter(is_read=False).count()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Follow(models.Model):
    follower = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('follower'),
    )
    following = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=_('following'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return f'{self.follower.username} is following {self.following.username}'

    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        unique_together = ('follower', 'following')


# Перечисление типов выносим наверх для чистоты кода
class NotificationType(models.TextChoices):
    LIKE = 'LIKE', _('Like')
    COMMENT = 'COMMENT', _('Comment')
    FOLLOW = 'FOLLOW', _('Follow')


# ВОТ ЭТА СТРОЧКА БЫЛА ПРОПУЩЕНА:
class Notification(models.Model):
    sender = models.ForeignKey(
        'users.UserModel',
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        verbose_name=_('sender'),
    )
    receiver = models.ForeignKey(
        'users.UserModel',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('receiver'),
    )
    notification_type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
        verbose_name=_('notification_type')
    )

    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('post'),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    is_read = models.BooleanField(default=False, verbose_name=_('is_read'))

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.notification_type})"

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')