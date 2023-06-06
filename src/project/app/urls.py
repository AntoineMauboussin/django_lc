from django.contrib import admin
from django.urls import path, include


from .views import (
    delete_item,
    index,
    create_item,
    items_list,
)
from .views import index, register, share_item, shared_items, delete_item

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register", register, name="register"),
    path("create_item", create_item, name="create_item"),
    path("items_list", items_list, name="items_list"),
    path("share_item/<int:id>", share_item, name="share_item"),
    path("shared_items", shared_items, name="shared_items"),
    path("delete_item/<int:id>", delete_item, name="delete_item"),
]
