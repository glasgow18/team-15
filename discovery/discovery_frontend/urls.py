from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from discovery_frontend import views

urlpatterns = [
    url("", views.hello)
]
