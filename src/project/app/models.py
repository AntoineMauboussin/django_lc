from django.db import models
from django.db.models import Model


class Prospect(Model):
    # 255 Limit CharField
    first_name = models.CharField(blank=False, null=False, max_length=255)
    last_name = models.CharField(blank=False, null=False, max_length=255)
    tel = models.CharField(blank=False, null=False, max_length=255)
    email = models.CharField(blank=False, null=False, max_length=255)
    message = models.TextField(blank=True, null=True)  # OK not this one
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

# Create your models here.
