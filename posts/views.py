from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from posts.models import Post, Comment, Like, CommentLike, CommentReply, ReplyCommentLike
from users.models import UserModel
from users.models import Notification


def explore(request):
    posts = Post.objects.exclude(post_type=Post.PostTypeChoice.History).order_by('-created_at')[:30]
    return render(request, 'explore.html', {'posts': posts})


def main_view(request):
    if request.user.is_authenticated:
        following = request.user.following.all()
        following_ids = [user.id for user in following]
    else:
        following_ids = []

    suggested_users = UserModel.objects.exclude(id__in=following_ids)

    post_filter = {"post_type": Post.PostTypeChoice.POST}
    if len(following_ids) > 3:
        post_filter['author__in'] = following_ids

    posts = Post.objects.filter(**post_filter).order_by('-created_at')

    if request.user.is_authenticated:
        posts = posts.exclude(author=request.user)

        user_likes = Like.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)

        for post in posts:
            post.is_liked = post.id in user_likes

    return render(request, 'index.html', {
        'posts': posts,
        'suggested_users': suggested_users,
    })



def reels_page(request):
    reels = (
        Post.objects.filter(
            post_type=Post.PostTypeChoice.Reels
        ).order_by('-created_at')
    )

    return render(request, 'reels.html', {'reels': reels})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comments'] = self.object.comments.select_related('user').prefetch_related(
            'comment_like',
            'reply_comment__reply_comment_likes'
        ).order_by('-created_at')

        return context


@login_required
def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            text=request.POST.get('text')
        )

        # УВЕДОМЛЕНИЕ: О новом комментарии
        if post.author != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                notification_type='COMMENT',
                post=post
            )

    return redirect("posts:post_detail", pk=post.pk)


@login_required
def reply_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        CommentReply.objects.create(
            user=request.user,
            post=comment.post,
            comment=comment,
            reply_comment=request.POST.get('reply_comment')
        )

        # УВЕДОМЛЕНИЕ: Ответ на комментарий
        if comment.user != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=comment.user,
                notification_type='COMMENT',  # Можно добавить отдельный тип REPLY
                post=comment.post
            )

    return redirect("posts:post_detail", pk=comment.post.pk)


@login_required
def toggle_post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(user=request.user, post=post).first()

    if like:
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)

        # УВЕДОМЛЕНИЕ: О лайке на пост
        if post.author != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                notification_type='LIKE',
                post=post
            )

    return redirect(request.GET.get("next", "/"))


@login_required
def toggle_comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    comment_like = CommentLike.objects.filter(user=request.user, comment=comment, post=comment.post).first()
    if comment_like:
        comment_like.delete()
    else:
        CommentLike.objects.create(user=request.user, comment=comment, post=comment.post)

        if comment.user != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=comment.user,
                notification_type='LIKE',
                post=comment.post
            )

    return redirect(request.GET.get("next", "/"))


@login_required
def toggle_reply_like(request, pk):
    reply = get_object_or_404(CommentReply, pk=pk)

    reply_comment_like = ReplyCommentLike.objects.filter(user=request.user, reply_comment=reply).first()
    if reply_comment_like:
        reply_comment_like.delete()
    else:
        ReplyCommentLike.objects.create(user=request.user, reply_comment=reply)

    return redirect(request.GET.get("next", "/"))


@login_required
def create_post_view(request):
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        post_type = request.POST.get('post_type', 'post')
        contentUrl = request.POST.get('contentUrl')

        if contentUrl:
            Post.objects.create(
                user=request.user,
                contentUrl=contentUrl,
                caption=caption,
                post_type=post_type
            )
            return redirect('users:profile')
    return render(request, 'create_post.html')


@login_required
def notifications_view(request):
    # Получаем все уведомления текущего пользователя, свежие — сверху
    notifications = request.user.notifications.all().order_by('-created_at')

    unread = notifications.filter(is_read=False)
    unread.update(is_read=True)

    return render(request, 'notifications.html', {'notifications': notifications})
