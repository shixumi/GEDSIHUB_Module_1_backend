# users/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_activation_email_task(email, activation_link):
    subject = "Activate your account"
    message = f"Click the following link to activate your account: {activation_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
