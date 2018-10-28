from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from discovery_frontend import views
from discovery import settings

urlpatterns = [
    url(r'^$', views.hello)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

