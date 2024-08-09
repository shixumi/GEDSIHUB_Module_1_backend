# users/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .serializers import UserSerializer
from .models import CustomUser
from .tasks import send_activation_email_task

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)  # Ensure the user is inactive until activation
        activation_link = self.get_activation_link(user)
        self.send_activation_email(user.email, activation_link)

    def get_activation_link(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return f"{settings.FRONTEND_URL}/activate/{uid}/{token}"

    def send_activation_email(self, email, activation_link):
        send_activation_email_task.delay(email, activation_link)
        

class ActivateAccountView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            reset_link = self.get_reset_link(user)
            self.send_reset_email(user.email, reset_link)
            return Response({"message": "Password reset link sent!"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_reset_link(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

    def send_reset_email(self, email, reset_link):
        subject = "Password Reset Request"
        message = f"Click the following link to reset your password: {reset_link}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            password = request.data.get("password")
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
