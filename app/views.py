from django.shortcuts import render

from .models import Post

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect

from .forms import PostForm

from django.shortcuts import redirect, get_object_or_404

from .models import User

from .forms import UserRegistrationForm

from .forms import UserLoginForm

from django.shortcuts import redirect

from django.contrib.auth import logout

from .forms import UserPasswordChangeForm

from .forms import UserPasswordResetForm

from .forms import UserPasswordResetConfirmForm


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'home.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post_create.html', context)


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('home')


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    return render(request, 'user_profile.html', context)


def user_follow(request, username):
    user = get_object_or_404(User, username=username)
    request.user.following.add(user)
    return redirect('user_profile', username=username)


def user_unfollow(request, username):
    user = get_object_or_404(User, username=username)
    request.user.following.remove(user)
    return redirect('user_profile', username=username)


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'user_registration.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'user_login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def user_password_change(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'user_password_change.html', context)


def user_password_reset(request):
    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserPasswordResetForm()
    context = {
        'form': form,
    }
    return render(request, 'user_password_reset.html', context)


def user_password_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        form = UserPasswordResetConfirmForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserPasswordResetConfirmForm(uidb64=uidb64, token=token)
    context = {
        'form': form,
    }
    return render(request, 'user_password_reset_confirm.html', context)