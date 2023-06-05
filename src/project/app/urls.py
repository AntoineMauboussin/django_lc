from django.contrib import admin
from django.urls import path, include


from .views import (
    index,
    create_item,
    items_list,
)
from .views import index, register

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register", register, name="register"),
    path("create_item", create_item, name="create_item"),
    path("items_list", items_list, name="items_list"),
]
