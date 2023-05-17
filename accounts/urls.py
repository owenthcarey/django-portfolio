from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("register/", views.register, name="register"),
]
