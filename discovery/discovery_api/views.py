from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, parsers, renderers
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from discovery_api.models import Location, Warnings, KeyWord, Activity, Comment
from discovery_api.search import SearchBar
from discovery_api.serializers import UserSerializer, LocationSerializer, CommentSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication





def print_result(annotations):
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return 0


def analyze(content):
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    return annotations




class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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


class CommentsView(ListAPIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    renderer_classes = (renderers.JSONRenderer,)
    def post(self, request, *args, **kwargs):
        comments = Comment.objects.filter(location_id=request.data['location'])
        return Response(CommentSerializer(comments, context={'request': request}, many=True).data, status=status.HTTP_200_OK)


class CreateCommentView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        comment = request.data['comment']
        location_id = request.data['id']
        new_activity = Comment.objects.create(content=comment, location=Location.objects.get(pk=location_id))
        annotations = (analyze(comment))
        score = annotations.document_sentiment.score
        print(score)
        if score > 0:
            return Response(CommentSerializer(new_activity, context={'request': request}).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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


class AddLocation(ListAPIView):
    def post(self, request):
        print(request)
        locname = request.data.get("locname", "")
        locaddr = request.data.get["address"]
        locprice = request.data["price"]
        locdesc = request.data["description"]

        location = Location(name=locname, free=True, price=locprice, description=locdesc, address=locaddr)

        location.save()

        return Response(status=status.HTTP_200_OK)


