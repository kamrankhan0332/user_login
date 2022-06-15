from rest_framework import serializers
from .models import UserProfile, User


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
