from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import CustomUser, Student, Employee

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=[('Student', 'Student'), ('Employee', 'Employee')])

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"email": e.message})

        if not value.endswith('@iskolarngbayan.pup.edu.ph'):
            raise serializers.ValidationError("Email must end with '@iskolarngbayan.pup.edu.ph'")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')

        if CustomUser.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        user = CustomUser.objects.create(
            email=validated_data.get('email'),
            is_active=False,
            role=role
        )
        user.set_password(password)
        user.save()

        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
