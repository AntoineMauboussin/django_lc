from django.contrib import admin
from .models import Item, SharedItem


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "user_name",
        "password",
        "url",
        "creation_date",
        "last_modification_date",
        "creation_user",
        "password_score",
    )


admin.site.register(Item, ItemAdmin)


class SharedItemAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "sending_user",
        "receiving_user",
        "creation_date",
    )


admin.site.register(SharedItem, SharedItemAdmin)

# Register your models here.
