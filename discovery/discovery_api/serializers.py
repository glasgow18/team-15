from django.contrib.auth.models import User, Group
from rest_framework import serializers

from discovery_api.models import Location


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'free', 'price', 'description', 'address')