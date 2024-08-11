# lmshub/analytics/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'analytics', AnalyticsViewSet)
router.register(r'report', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
