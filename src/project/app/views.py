from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from cryptography.fernet import Fernet
import base64

from app.forms import RegisterForm
from django.contrib.auth.models import User

from .models import Item

import secrets

secret_key = "1c8FXcuaHL9qV3Zf5263TR_fU37dfkz9CU_O1ZFyno8="
# encoded_key = base64.urlsafe_b64encode(secret_key)
crypter = Fernet(secret_key.encode())

key = Fernet.generate_key()
print("Key : ", key.decode())
f = Fernet(key)
encrypted_data = f.encrypt(b"This message is being encrypted and cannot be seen!")
print("After encryption : ", encrypted_data)
decrypted_data = f.decrypt(encrypted_data)
print(decrypted_data)
print("After decryption : ", decrypted_data.decode())


def index(request):
    return render(request, "index.html")


def register(request):
    validation = False

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                form.cleaned_data["username"], "", form.cleaned_data["password1"]
            )
            validation = True

    else:
        form = RegisterForm()

    context = {"form": form, "validation": validation}
    return render(request, "registration/register.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def create_item(request):
    if request.method == "POST":
        user_name = crypter.encrypt(request.POST.get("username").encode()).decode()
        password = crypter.encrypt(request.POST.get("password").encode()).decode()
        url = crypter.encrypt(request.POST.get("url").encode()).decode()
        creation_user = request.user

        item_object = Item.objects.create(
            user_name=user_name, password=password, url=url, creation_user=creation_user
        )
        item_object.save()

        return redirect("items_list")

    return render(request, "form_item_prospect.html", context={})


@login_required
@require_http_methods(["GET", "POST"])
def update_item(request, item_id):
    Item.objects.get
    item = Item.objects.get(id=item_id)

    if request.method == "POST":
        item.user_name = crypter.encrypt(request.POST.get("username").encode()).decode()
        item.password = crypter.encrypt(request.POST.get("password").encode()).decode()
        item.url = crypter.encrypt(request.POST.get("url").encode()).decode()

        item.save()

        return redirect("items_list")

    reverse_url = reverse("update_item", args=[item.id])

    item.user_name = crypter.decrypt(item.user_name.encode()).decode()
    item.password = crypter.decrypt(item.password.encode()).decode()
    item.url = crypter.decrypt(item.url.encode()).decode()

    return render(
        request,
        "form_item_update.html",
        context={"item": item, "reverse_url": reverse_url},
    )


@login_required
def delete_item(request, item_id):
    item = Item.objects.filter(id=item_id)
    item.delete()
    return redirect(reverse("items_list"))


@login_required
def items_list(request):
    items = Item.objects.filter(creation_user=request.user)

    for item in items:
        item.user_name = crypter.decrypt(item.user_name.encode()).decode()
        item.password = crypter.decrypt(item.password.encode()).decode()
        item.url = crypter.decrypt(item.url.encode()).decode()

    return render(request, "items_list.html", context={"items": items})
