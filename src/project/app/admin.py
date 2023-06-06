from django.contrib import admin
from .models import Prospect, SharedItem


class ProspectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "tel",
        "email",
        "created",
        "updated",
    )

    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "tel",
        "email",
        "created",
        "updated",
        "message",
    )

admin.site.register(Prospect, ProspectAdmin)

class SharedItemAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "sending_user",
        "receiving_user",
        "creation_date",
    )

admin.site.register(SharedItem, SharedItemAdmin)

# Register your models here.
