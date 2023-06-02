from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from django import forms
from app.forms import RegisterForm
from django.contrib.auth.models import User

def index(request):
    # return HttpResponse(f"Hi")
    return render(request, "index.html")

def register(request):
    validation = False

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password1'])
            validation = True
    
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'validation': validation
    }

    return render(request, 'registration/register.html', context)