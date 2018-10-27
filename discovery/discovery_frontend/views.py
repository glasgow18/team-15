from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from discovery_frontend.models import Location


def hello(req):
    # some random code to search for stuff
    search_result = Location.objects.all()
    return render(req, "inherits.html", context={'result': search_result})
