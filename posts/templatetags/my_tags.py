from django import template

from posts.models import Like, CommentLike, ReplyCommentLike
from users.models import Follow

register = template.Library()


@register.simple_tag
def post_heart_icon(request, post):
    return "fa-solid fa-heart" if Like.objects.filter(user=request.user, post=post).exists() else "fa-regular fa-heart"


@register.simple_tag
def post_comment_heart_icon(request, comment):
    return "fa-solid fa-heart" if CommentLike.objects.filter(user=request.user, comment=comment,
                                                             post=comment.post).exists() else "fa-regular fa-heart"


@register.simple_tag
def reply_comment_heart_icon(request, reply_comment):
    return "fa-solid fa-heart" if ReplyCommentLike.objects.filter(
        user=request.user,
        reply_comment=reply_comment).exists() else "fa-regular fa-heart"


@register.filter
def is_following(request, user):
    if not request.user.is_authenticated:
        return False

    return Follow.objects.filter(
        follower=request.user,
        following=user
    ).exists()

