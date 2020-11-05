from django.shortcuts import render
from django.http import HttpResponse
from www.models import Poll, Choice, TextPost


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def album(request, albumId):
    print('albumId', albumId)
    return render(request, "album.html", {})
