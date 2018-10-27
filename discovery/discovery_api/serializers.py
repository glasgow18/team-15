from django.contrib.auth.models import User, Group
from rest_framework import serializers

from discovery_api.models import Location, ContactDetail, Category, Activity, Warnings, KeyWord, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class LocationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print(validated_data)

        obj = Location.objects.create(**validated_data)
        obj.save()
        return obj

    # def create(self, request, *args, **kwargs):
    #     raw_data = request.data
    #     serializer = self.get_serializer(data=raw_data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()  # Include the user when saving.

    class Meta:
        model = Location
        fields = (
        'name', 'free', 'price', 'description', 'address', 'contact', 'possibleActivities', 'keyWords', 'warnings',
        'activities')


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
