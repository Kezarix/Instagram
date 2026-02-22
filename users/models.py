from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True, blank=True
    )
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f'{self.first_name} {self.last_name}'


class Follow(models.Model):
    follower = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} is following {self.following.username}'

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        unique_together = ('follower', 'following')


