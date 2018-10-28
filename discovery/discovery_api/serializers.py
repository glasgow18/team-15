from django.contrib.auth.models import User, Group
from rest_framework import serializers

from discovery_api.models import Location, ContactDetail, Category, Activity, Warnings, KeyWord, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class LocationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        temp_keywords = validated_data['keyWords']
        temp_activities = validated_data['activities']
        temp_warnings = validated_data['warnings']
        del validated_data['keyWords']
        del validated_data['activities']
        del validated_data['warnings']

        obj = Location.objects.create(**validated_data)
        for keyword in temp_keywords:
            obj.keyWords.add(keyword)
        for activity in temp_activities:
            obj.activities.add(activity)
        for warning in temp_warnings:
            obj.warnings.add(warning)

        obj.save()
        return obj

    class Meta:
        model = Location
        fields = (
            'name', 'free', 'price', 'description', 'address', 'contact', 'possibleActivities', 'keyWords', 'warnings',
            'activities', 'lat', 'long','picture')


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
