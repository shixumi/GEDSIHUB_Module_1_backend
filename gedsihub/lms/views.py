# lmshub/lms/views.py
from rest_framework import viewsets
from .models import Course, Module, Content, Assessment, Certificate, Enrollment, Flair
from .serializers import CourseSerializer, ModuleSerializer, ContentSerializer, AssessmentSerializer, CertificateSerializer, EnrollmentSerializer, FlairSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class FlairViewSet(viewsets.ModelViewSet):
    queryset = Flair.objects.all()
    serializer_class = FlairSerializer
