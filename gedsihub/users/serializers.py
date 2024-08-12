from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import CustomUser, Student, Employee
from django.utils import timezone

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

        role = self.initial_data.get('role')
        if role == 'Student' and not value.endswith('@iskolarngbayan.pup.edu.ph'):
            raise serializers.ValidationError("Student email must end with '@iskolarngbayan.pup.edu.ph'")
        elif role == 'Employee' and not value.endswith('@pup.edu.ph'):
            raise serializers.ValidationError("Employee email must end with '@pup.edu.ph'")

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
    phone_number = serializers.CharField(
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )

    class Meta:
        model = Student
        fields = '__all__'
    
    def validate(self, data):
        # Custom validation logic
        if 'year' in data and not data['year'].isdigit():
            raise serializers.ValidationError({'year': 'Year must be a number'})
        if 'birthday' in data and data['birthday'] > timezone.now().date():
            raise serializers.ValidationError({'birthday': 'Birthday cannot be a future date'})
        return data

class EmployeeSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    
    class Meta:
        model = Employee
        fields = '__all__'

    def validate(self, data):
        # Custom validation logic
        if 'birthday' in data and data['birthday'] > timezone.now().date():
            raise serializers.ValidationError({'birthday': 'Birthday cannot be a future date'})
        return data
