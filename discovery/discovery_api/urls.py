from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from discovery_api import views
from discovery_api.views import SearchView, SearchBarView, AddLocation

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'locations', views.LocationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url('/', include(router.urls)),
    url('search/', SearchView.as_view()),
    url('search_bar/', SearchBarView.as_view()),
    url('addlocation/', AddLocation.as_view()),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
