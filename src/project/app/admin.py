from django.contrib import admin
from .models import Prospect


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

# Register your models here.
