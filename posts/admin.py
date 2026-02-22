from django.contrib import admin

from posts.models import Post, Like, Comment, CommentLike, CommentReply, ReplyCommentLike

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(CommentReply)
admin.site.register(ReplyCommentLike)

