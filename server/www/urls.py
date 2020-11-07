from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('hello', views.hello),
    path('image/<str:imagePath>/<str:imageFileName>', views.images),
    path('album/<str:albumTitle>', views.albums, name='index'), ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
