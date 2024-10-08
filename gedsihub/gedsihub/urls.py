# gedsihub/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# gedsihub/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),  # Include users app URLs
    path('api/lms/', include('lms.urls')),  # Include LMS app URLs
    path('api/analytics/', include('analytics.urls')), # Include Analytics app URLS
    path('api/forum/', include('forum.urls')), # Include Analytics app URLS
    path('api/chatbot/', include('chatbot.urls')), # Include Analytics app URLS
]


# gedsihub/urls.py
