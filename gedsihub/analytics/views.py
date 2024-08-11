# lmshub/analytics/views.py

from rest_framework import viewsets
from .models import Analytics, Report
from .serializers import AnalyticsSerializer, ReportSerializer

class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
