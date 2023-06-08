from django.contrib import admin
from django.urls import path, include


from .views import (
    delete_item,
    display_password,
    index,
    create_item,
    items_list,
    update_item,
    delete_item,
)
from .views import index, register, share_item, shared_items, delete_item,delete_shared, change_username

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register", register, name="register"),
    path("create_item", create_item, name="create_item"),
    path("items_list", items_list, name="items_list"),
    path("share_item/<int:id>", share_item, name="share_item"),
    path("shared_items", shared_items, name="shared_items"),
    path("delete_shared/<int:id>", delete_shared, name="delete_shared"),
    path("update_item/<item_id>", update_item, name="update_item"),
    path("delete_item/<item_id>", delete_item, name="delete_item"),
    path("display_password/<int:id>", display_password, name="display_password"),
    path('changedmymind/', change_username, name='changedmymind'),
]
