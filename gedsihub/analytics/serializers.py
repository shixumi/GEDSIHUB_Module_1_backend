# lmshub/analytics/serializers.py

from rest_framework import serializers
from .models import Analytics, Report
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'sex', 'gender_identity', 'preferred_pronoun', 'indigenous_cultural_community', 'differently_abled']

class AnalyticsSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Include user details

    class Meta:
        model = Analytics
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
