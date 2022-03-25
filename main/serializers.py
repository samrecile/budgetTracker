from rest_framework import serializers
from .models import Profile, daily, asset, liability, recurring

class profileSerializer(serializer.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['userId', 'cash']

class dailySerializer(serializer.ModelSerializer):
    class Meta:
        model = daily
        fields = ['income', 'restExp', 'grocExp', 'gasExp', 'uberExp', 'alcExp', 'barberExp', 'barExp', 'discExp', 'stockExp', 'cryptoExp', 'debtExp']

class assetSerializer(serializer.ModelSerializer):
    class Meta:
        model = asset
        fields = ['name', 'value', 'depreciation', 'appreciation']

class liabilitySerializer(serializer.ModelSerializer):
    class Meta:
        model = liability
        fields = ['name', 'value', 'interest', 'payment']

class recurringSerializer(serializer.ModelSerializer):
     class Meta:
        model = recurring
        fields = ['name', 'category', 'value']