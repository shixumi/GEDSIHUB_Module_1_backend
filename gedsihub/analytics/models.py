# lmshub/analytics/models.py

from django.db import models
from users.models import CustomUser  # Import CustomUser

class Analytics(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use CustomUser instead of UserData
    module = models.CharField(max_length=100)
    time_spent = models.FloatField()  # Time spent in hours
    completion_status = models.BooleanField(default=False)
    date_recorded = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)
