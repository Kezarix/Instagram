from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from posts.models import Post
from users.forms import RegisterForm, LoginForm
from users.models import UserModel, Follow


def registration_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, "register.html", context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('users:profile')
    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, "login.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required
def profile_view(request):
    user = request.user
    posts = user.posts.all().order_by('-created_at')

    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, "profile.html", context)


def another_profile_view(request, pk):
    user = get_object_or_404(UserModel, pk=pk)
    posts = user.posts.all().order_by('-created_at')
    return render(request, 'profile.html', {'user': user, 'posts': posts})


@login_required
def follow(request, pk):
    user = UserModel.objects.get(pk=pk)
    follow_user = Follow.objects.filter(follower=request.user, following=user).first()

    if not request.user == user and not follow_user:
        Follow.objects.create(
            follower=request.user,
            following=user
        )
    return redirect(request.GET.get('next', '/'))


@login_required
def unfollow(request, pk):
    user = UserModel.objects.get(pk=pk)

    if not request.user == user:
        follow = Follow.objects.filter(
            follower=request.user,
            following=user
        ).first()

        if follow:
            follow.delete()

    return redirect(request.GET.get('next', '/'))


def people_search(request):
    q = request.GET.get('q', '')
    users = UserModel.objects.filter(
        Q(username__icontains=q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q)
    )
    return render(request, 'search.html', {'users': users})
