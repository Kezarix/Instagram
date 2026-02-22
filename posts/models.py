from django.db import models

from users.models import UserModel


class Post(models.Model):
    class PostTypeChoice(models.TextChoices):
        History = 'HISTORY', 'History'
        Post = 'POST', 'Post'
        Reels = 'REELS', 'Reels'

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    post_type = models.CharField(max_length=10, choices=PostTypeChoice)
    contentUrl = models.FileField(upload_to='posts/')
    caption = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtag = models.TextField(null=True, blank=True)
    location = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'Пост от {self.author.username}'


class Like(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked post '


class Comment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'


class CommentLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comment_like')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_like')

    def __str__(self):
        return self.user.username


class CommentReply(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reply_comment')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reply_comment')
    reply_comment = models.TextField()

    def __str__(self):
        return f'Comment by {self.user.username}'


class ReplyCommentLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reply_comment_likes')
    reply_comment = models.ForeignKey(CommentReply, on_delete=models.CASCADE, related_name='reply_comment_likes')
