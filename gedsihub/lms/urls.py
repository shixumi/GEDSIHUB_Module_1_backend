from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    ModuleViewSet,
    ContentViewSet,
    AssessmentViewSet,
    CertificateViewSet,
    EnrollmentViewSet,
    FlairViewSet,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'certificates', CertificateViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'flairs', FlairViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
