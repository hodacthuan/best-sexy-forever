from django.shortcuts import render
from django.http import HttpResponse
from pageScrape.models import Album
import pageScrape
from pageScrape.commons import dataLogging
from sexybaby import constants


def index(request):
    return HttpResponse("Hello, world. ")


def album(request, albumId):
    print('albumId', albumId)
    album = Album.objects(id=albumId)[0]
    print(album.thumbnail.sourceUrl)
    album.thumbnail.url = constants.BUCKET_PUBLIC_URL + \
        album.thumbnail.storePath
    for index in range(len(album.images)):

        album.images[index].url = constants.BUCKET_PUBLIC_URL + \
            album.images[index].storePath

    print(album.images[1].url)
    # dataLogging(album, '')

    context = {
        'album': album
    }
    return render(request, "album.html", context)
