from django.http import HttpResponse

def squares(request):
    x = []
    for i in range(10):
        x.append(str(i**2))
    return HttpResponse(f"<p>{'<br>'.join(x)}</p>")