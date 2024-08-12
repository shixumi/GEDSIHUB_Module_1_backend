from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .serializers import CustomUserSerializer, StudentSerializer, EmployeeSerializer
from .models import CustomUser, Student, Employee
from rest_framework.exceptions import ValidationError

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        activation_link = self.get_activation_link(user)
        print(f"Activation link generated: {activation_link}")  # Debugging line
        self.send_activation_email(user.email, activation_link)

    def get_activation_link(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return f"{settings.FRONTEND_URL}/api/users/activate/{uid}/{token}"

    def send_activation_email(self, email, activation_link):
        subject = "Activate your account"
        message = f"Click the following link to activate your account: {activation_link}"
        try:    
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            print(f"Activation email sent to {email}")  # Debugging line
        except Exception as e:
            print(f"Error sending activation email: {e}")  # Debugging line

class UserProfileCompletionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if hasattr(user, 'student'):
            return StudentSerializer
        elif hasattr(user, 'employee'):
            return EmployeeSerializer
        return None

    def post(self, request):
        serializer_class = self.get_serializer_class()
        if not serializer_class:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

        profile = self.get_user_profile()
        serializer = serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_user_profile(self):
        user = self.request.user
        if user.role == 'Student':
            return user.student
        elif user.role == 'Employee':
            return user.employee
        raise ValidationError("Profile not found for the user.")

class ActivateAccountView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"message": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            
            # Profile creation based on role
            if user.role == 'Student':
                Student.objects.get_or_create(user=user)
            elif user.role == 'Employee':
                Employee.objects.get_or_create(user=user)
            
            return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        reset_link = self.get_reset_link(user)
        self.send_reset_email(email, reset_link)
        return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)

    def get_reset_link(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

    def send_reset_email(self, email, reset_link):
        subject = "Reset your password"
        message = f"Click the following link to reset your password: {reset_link}"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            password = request.data.get("password")
            if not password:
                return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
