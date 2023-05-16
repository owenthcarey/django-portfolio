from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


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
