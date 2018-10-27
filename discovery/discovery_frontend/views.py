from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from discovery_frontend.forms import AddLocationForm
from discovery_api.models import Location


def hello(req):
    # some random code to search for stuff
    search_result = Location.objects.all()
    add_location_form = AddLocationForm()

    return render(req, "inherits.html", context={'form': add_location_form})
