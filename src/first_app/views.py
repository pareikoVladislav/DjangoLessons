from django.http import HttpResponse


def greetings(request):
    return HttpResponse("<h1>Hello, world!</h1>")
