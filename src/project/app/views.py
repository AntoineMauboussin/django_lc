from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from django.contrib.auth.decorators import login_required


def index(request):
    # return HttpResponse(f"Hi")
    return render(request, "index.html")


def compute_square(request, number):
    square = number * number
    context = {"square": square, "number": number}
    return render(request, "compute_square.html", context=context)


def compute_squares(request, number):
    numbers = list(range(number))
    squares = [n**2 for n in numbers]
    context = {
        "number_and_square": [
            {"number": number, "square": square}
            for number, square in zip(numbers, squares)
        ]
    }
    return render(request, "compute_squares.html", context=context)


def random_wiki(request):
    req = Request(
        "https://en.wikipedia.org/wiki/Special:RandomInCategory/Featured_articles",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, "html.parser")
    title = soup.title.string
    lang = []
    for link in soup.select(".interlanguage-link a"):
        lang.append(link.get_text())

    context = {"lang": lang, "title": title}
    return render(request, "random_wiki.html", context=context)


from .models import Prospect, Item


@require_http_methods(["GET", "POST"])
def form_prospect(request):
    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        tel = request.POST.get("tel")
        email = request.POST.get("email")
        message = request.POST.get("message")

        prospect_object = Prospect.objects.create(
            first_name=first_name,
            last_name=last_name,
            tel=tel,
            email=email,
            message=message,
        )
        prospect_object.save()

        return render(request, "form_received.html")
    return render(request, "form_prospect.html", context={})


@login_required
@require_http_methods(["GET", "POST"])
def create_item(request):
    if request.method == "POST":
        print(request.POST)
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        url = request.POST.get("url")
        creation_user = request.user

        item_object = Item.objects.create(
            user_name=user_name, password=password, url=url, creation_user=creation_user
        )
        item_object.save()

        return redirect("items_list")

    return render(request, "form_item_prospect.html", context={})


@login_required
def items_list(request):
    items = Item.objects.filter(creation_user=request.user)
    return render(request, "items_list.html", context={"items": items})
