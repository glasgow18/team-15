from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, parsers, renderers
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from discovery_api.models import Location, Warnings, KeyWord, Activity
from discovery_api.search import SearchBar
from discovery_api.serializers import UserSerializer, LocationSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):

        # pull warnings from request
        warning_names = request.data["warnings"].lower().split(", ")
        actual_warnings = []
        for warning_name in warning_names:
            existing_warnings = Warnings.objects.filter(name=warning_name.strip())
            if len(existing_warnings) != 0:
                actual_warnings.append(existing_warnings.first().id)
            else:
                new_warning = Warnings.objects.create(name=warning_name.strip())
                new_warning.save()
                actual_warnings.append(new_warning.id)

        request.data["warnings"] = actual_warnings

        # pull keywords from request
        actual_keywords = []
        keyword_names = request.data["keyWords"].lower().split(", ")
        for keyword_name in keyword_names:
            existing_keywords = KeyWord.objects.filter(tag=keyword_name.strip())
            if len(existing_keywords) != 0:
                actual_keywords.append(existing_keywords.first().id)
            else:
                new_keyword = KeyWord.objects.create(tag=keyword_name.strip())
                new_keyword.save()
                actual_keywords.append(new_keyword.id)

        request.data["keyWords"] = actual_keywords

        actual_activities = []
        activity_names = request.data["activities"].lower().split(", ")

        for activity_name in activity_names:
            existing_activities = Activity.objects.filter(name=activity_name.strip())
            if len(existing_activities) != 0:
                actual_activities.append(existing_activities.first().id)
            else:
                new_activity = Activity.objects.create(name=activity_name.strip())
                new_activity.save()
                actual_activities.append(new_activity.id)

        request.data["activities"] = actual_activities

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class SearchView(ListAPIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        category = request.data['category']
        activity = request.data['activity']

        locationsByCategory = Location.objects.filter(activities__category_id=category).all() if str(
            category).isdigit() else None
        locationsByActivity = Location.objects.filter(activities__id=activity).all() if str(
            activity).isdigit() else None

        print(locationsByCategory)
        print(locationsByActivity)
        locations = locationsByCategory.intersection(
            locationsByActivity) if locationsByCategory is not None and locationsByActivity is not None else locationsByCategory if locationsByCategory is not None else locationsByActivity

        print(locationsByCategory)
        return Response(LocationSerializer(locations, context={'request': request}, many=True).data,
                        status=status.HTTP_200_OK)

class SearchBarView(ListAPIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        locations=SearchBar.search_str(request.data['filter'])
        return Response(LocationSerializer(locations, context={'request': request}, many=True).data,status=status.HTTP_200_OK)
