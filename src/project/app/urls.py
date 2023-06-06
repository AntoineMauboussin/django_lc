from django.contrib import admin
from django.urls import path, include


from .views import (
    index,
    create_item,
    items_list,
    update_item,
    delete_item,
)
from .views import index, register

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register", register, name="register"),
    path("create_item", create_item, name="create_item"),
    path("items_list", items_list, name="items_list"),
    path("update_item/<item_id>", update_item, name="update_item"),
    path("delete_item/<item_id>", delete_item, name="delete_item"),
]
