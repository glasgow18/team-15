from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from discovery_frontend.forms import AddLocationForm
from discovery_api.models import Location, Category, Activity


def hello(req):
    # some random code to search for stuff
    search_result = Location.objects.all()
    add_location_form = AddLocationForm()
    categories = Category.objects.all()
    activities = Activity.objects.all()
    return render(req, "inherits.html", context={'form': add_location_form, 'categories': categories, 'activities':activities})
