from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from cryptography.fernet import Fernet
from django.contrib import messages

from django import forms
from app.forms import RegisterForm, ShareForm
from django.contrib.auth.models import User

secret_key = "1c8FXcuaHL9qV3Zf5263TR_fU37dfkz9CU_O1ZFyno8="
crypter = Fernet(secret_key.encode())

from .utils import calculate_password_score
from .models import Item, SharedItem


def index(request):
    return render(request, "index.html")


def register(request):
    validation = False

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            existing_user = User.objects.filter(
                username=form.cleaned_data["username"]
            ).exists()

            if existing_user:
                messages.error(request, "Username is already in use.")
            else:
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
        password_score = calculate_password_score(request.POST.get("password"))

        item_object = Item.objects.create(
            user_name=user_name,
            password=password,
            url=url,
            creation_user=creation_user,
            password_score=password_score,
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

        item.password_score = calculate_password_score(request.POST.get("password"))

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

    shared_items = SharedItem.objects.filter(receiving_user=request.user)
    has_shared_items = shared_items.exists()
    return render(
        request,
        "items_list.html",
        context={
            "items": items,
            "shared_items": shared_items,
            "has_shared_items": has_shared_items,
        },
    )


@login_required
def share_item(request, id):
    item = Item.objects.filter(id=id)
    validation = ""

    if not item.exists():
        context = {"validation": "Invalid Url"}
        return render(request, "share_item.html", context)

    if request.method == "POST":
        form = ShareForm(request.POST)

        if not (form.is_valid()):
            context = {"validation": "A problem has occurred"}
            return render(request, "share_item.html", context)

        receiver = User.objects.filter(username=form.cleaned_data["username"])
        item = Item.objects.filter(id=id)

        if receiver.exists() and receiver.first() != request.user:
            shared_existing = SharedItem.objects.filter(
                item=item.first(), receiving_user=receiver.first()
            )

            print(shared_existing)

            if not (shared_existing.exists()):
                shared_item = SharedItem.objects.create(
                    item=item.first(),
                    sending_user=request.user,
                    receiving_user=receiver.first(),
                )
                shared_item.save()
                validation = "Password has been successfully shared"

            else:
                validation = "You already have shared this password to this user"

        else:
            validation = "This user does not exist or is invalid"

    else:
        form = ShareForm()

    context = {"form": form, "validation": validation}

    return render(request, "share_item.html", context)


@login_required
def shared_items(request):
    shared_items = SharedItem.objects.filter(sending_user=request.user)

    for shared_item in shared_items:
        shared_item.item.user_name = crypter.decrypt(
            shared_item.item.user_name.encode()
        ).decode()
        shared_item.item.password = crypter.decrypt(
            shared_item.item.password.encode()
        ).decode()
        shared_item.item.url = crypter.decrypt(shared_item.item.url.encode()).decode()

    return render(request, "shared_items.html", context={"shared_items": shared_items})


@login_required
def delete_shared(request, id):
    shared_item = SharedItem.objects.filter(id=id)

    if shared_item.exists() and shared_item.first().sending_user == request.user:
        shared_item.delete()

    return redirect("shared_items")


@login_required
def change_username(request):
    if request.method == "POST":
        new_username = request.POST.get("new_username")

        existing_user = User.objects.filter(username=new_username).exists()
        if existing_user:
            messages.error(request, "Username is already in use.")
        else:
            user = request.user
            user.username = new_username
            user.save()
            return redirect("index")

    return render(request, "change_username.html")
