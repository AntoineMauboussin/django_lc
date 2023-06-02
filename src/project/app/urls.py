from django.contrib import admin
from django.urls import path


from .views import index,compute_square,compute_squares,random_wiki,form_prospect

urlpatterns = [
    path("", index, name="index"),
    path("compute_square/<int:number>", compute_square, name="compute_square"),
    path("compute_squares/<int:number>", compute_squares, name="compute_squares"),
    path("random_wiki", random_wiki, name="random_wiki"),
    path("form_prospect", form_prospect, name="form_prospect")
]