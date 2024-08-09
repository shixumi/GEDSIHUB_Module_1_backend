# users/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        # Validate the email format and domain
        email_validator = EmailValidator()
        try:
            email_validator(value)  # Corrected this line to actually validate the email
        except DjangoValidationError as e:
            raise serializers.ValidationError({"email": e.message})
        
        if not value.endswith('@iskolarngbayan.pup.edu.ph'):
            raise serializers.ValidationError("Email must be a school email ending with '@iskolarngbayan.pup.edu.ph'")
        
        return value

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
