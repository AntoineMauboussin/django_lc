from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User


# Create your models here.
class Item(Model):
    user_name = models.CharField(blank=False, null=False, max_length=255)
    password = models.CharField(blank=False, null=False, max_length=255)
    url = models.CharField(blank=False, null=False, max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    password_score = models.CharField(blank=False, null=True, max_length=255)


class SharedItem(Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sending_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sending_%(class)s"
    )
    receiving_user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
