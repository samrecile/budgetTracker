from rest_framework import serializers
from .models import Profile, daily, asset, liability, recurring

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['userId', 'cash']

class dailySerializer(serializers.ModelSerializer):
    class Meta:
        model = daily
        fields = ['income', 'restExp', 'grocExp', 'gasExp', 'uberExp', 'alcExp', 'barberExp', 'barExp', 'discExp', 'stockExp', 'cryptoExp', 'debtExp']

class assetSerializer(serializers.ModelSerializer):
    class Meta:
        model = asset
        fields = ['name', 'value', 'depreciation', 'appreciation']

class liabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = liability
        fields = ['name', 'value', 'interest', 'payment']

class recurringSerializer(serializers.ModelSerializer):
     class Meta:
        model = recurring
        fields = ['name', 'category', 'value']