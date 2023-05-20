from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import Blog
from photos.models import Photo


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/profile.html")


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home:index")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_blogs = Blog.objects.filter(author=user)
    user_photos = Photo.objects.filter(author=user)
    context = {"profile_user": user, "user_blogs": user_blogs, "user_photos": user_photos}
    return render(request, "accounts/user_profile.html", context)
