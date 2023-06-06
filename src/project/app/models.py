from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User


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
class Item(Model):
    user_name = models.CharField(blank=False, null=False, max_length=255)
    password = models.CharField(blank=False, null=False, max_length=255)
    url = models.CharField(blank=False, null=False, max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE)

class SharedItem(Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sending_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sending_%(class)s')
    receiving_user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
