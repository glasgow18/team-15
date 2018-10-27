from django.contrib.auth.models import User, Group
from rest_framework import serializers

from discovery_api.models import Location, ContactDetail, Category, Activity, Warnings, KeyWord, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'free', 'price', 'description', 'address', 'contact')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = ('name', 'email', 'url', 'contactNumber1', 'contactNumber2')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name'


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('name', 'category')


class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warnings
        fields = ('name', 'category')


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = ('tag', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('userName', 'location', 'reviewDescription')
