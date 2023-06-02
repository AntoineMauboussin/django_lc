from django.contrib import admin
from django.urls import path, include


from .views import index,register

urlpatterns = [
    path("", index, name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', register, name="register"),
]