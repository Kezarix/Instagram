from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Dialog, Message


@login_required
def inbox(request):
    # Получаем все диалоги пользователя и сортируем по обновлению
    dialogs = request.user.dialogs.all().order_by('-updated_at')

    dialogs_with_other = []
    for d in dialogs:
        dialogs_with_other.append({
            "dialog": d,
            "other_user": d.other_user(request.user)
        })

    return render(request, "inbox.html", {"dialogs_with_other": dialogs_with_other})


@login_required
def start_dialog(request, user_id):
    User = get_user_model()
    other = get_object_or_404(User, id=user_id)

    dialog = Dialog.objects.filter(users=request.user) \
        .filter(users=other).first()

    if not dialog:
        dialog = Dialog.objects.create()
        dialog.users.add(request.user, other)

    return redirect('direct:dialog', dialog_id=dialog.id)


@login_required
def dialog(request, dialog_id):
    dialog_obj = get_object_or_404(Dialog, id=dialog_id, users=request.user)
    messages = dialog_obj.messages.select_related('sender').order_by('created_at')

    from posts.models import Post

    parsed_messages = []

    for m in messages:
        msg_data = {
            "sender": m.sender,
            "text": m.text,
            "is_share": False,
            "post": None
        }

        if m.text.startswith("SHARE_POST:"):
            try:
                post_id = int(m.text.split(":")[1])
                post = Post.objects.get(id=post_id)

                msg_data["is_share"] = True
                msg_data["post"] = post
            except:
                pass

        parsed_messages.append(msg_data)

    all_dialogs = request.user.dialogs.all().order_by('-updated_at')

    dialogs_with_other = []
    for d in all_dialogs:
        dialogs_with_other.append({
            "dialog": d,
            "other_user": d.other_user(request.user)
        })

    return render(request, 'dialog.html', {
        'dialog': dialog_obj,
        'messages': parsed_messages,
        'dialogs_with_other': dialogs_with_other,
        'other_user': dialog_obj.other_user(request.user)
    })


@login_required
def send_message(request, dialog_id):
    dialog = get_object_or_404(Dialog, id=dialog_id, users=request.user)

    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')

        if text or image:
            Message.objects.create(
                dialog=dialog,
                sender=request.user,
                text=text,
                image=image
            )
            dialog.save()

    return redirect('direct:dialog', dialog_id=dialog.id)


def my_chats_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        dialogs = request.user.dialogs.all()

        data = []
        for d in dialogs:
            opponent = d.other_user(request.user)
            if opponent:
                avatar_url = '/static/default.png'
                if hasattr(opponent, 'avatar') and opponent.avatar:
                    try:
                        avatar_url = opponent.avatar.url
                    except:
                        pass

                data.append({
                    'dialog_id': str(d.id),
                    'username': opponent.username,
                    'avatar': avatar_url
                })

        return JsonResponse(data, safe=False)
    except Exception as e:

        print(f"API Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
