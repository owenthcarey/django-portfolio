from django.urls import path
from . import views

urlpatterns = [
    path("generate_app_icon/", views.generate_app_icon, name="generate_app_icon"),
    path("generate_image/", views.generate_image, name="generate_image"),
]
