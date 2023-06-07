from django.urls import path
from django.contrib import admin
from shortener.index.views import index, register, login_view, logout_view, get_user, list_view


urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("get_user/<int:user_id>", get_user),
    path("list/", list_view, name="list_view"),
]
