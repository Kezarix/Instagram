from django.db import models

from users.models import UserModel
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    class PostTypeChoice(models.TextChoices):
        HISTORY = 'HISTORY', _('History')
        POST = 'POST', _('Post')
        REELS = 'REELS', _('Reels')

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('author')
    )

    post_type = models.CharField(
        max_length=10,
        choices=PostTypeChoice.choices,
        verbose_name=_('post type')
    )

    contentUrl = models.FileField(
        upload_to='posts/',
        verbose_name=_('content url')
    )

    caption = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('caption')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    hashtag = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('hashtag')
    )

    location = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('location')
    )

    def __str__(self):
        return f'Post by {self.author.username}'

class Like(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('user')
    )

    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('post')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    def __str__(self):
        return f'{self.user.username} liked post '


class Comment(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('user')
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('post')
    )

    text = models.TextField(verbose_name=_('text'))

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    def __str__(self):
        return f'Comment by {self.user.username}'


class CommentLike(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comment_like',
        verbose_name=_('user')
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_like',
        verbose_name=_('comment')
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment_like',
        verbose_name=_('post')
    )

    def __str__(self):
        return self.user.username


class CommentReply(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='reply_comment',
        verbose_name=_('user')
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='reply_comment',
        verbose_name=_('comment')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reply_comment',
        verbose_name=_('post')
    )

    reply_comment = models.TextField(
        verbose_name=_('reply comment')
    )

    def __str__(self):
        return f'Comment by {self.user.username}'


class ReplyCommentLike(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='reply_comment_likes',
        verbose_name=_('user')
    )

    reply_comment = models.ForeignKey(
        CommentReply,
        on_delete=models.CASCADE,
        related_name='reply_comment_likes',
        verbose_name=_('reply comment')
    )



