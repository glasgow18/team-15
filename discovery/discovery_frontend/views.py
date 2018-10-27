from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def hello(req):
    # some random code to search for stuff
    search_result = "some result"
    return render(req, "inherits.html", context={'result': search_result})
