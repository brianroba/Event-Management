from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RegisterView, home
from rest_framework.authtoken import views as drf_views

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', home, name='home'),  # Root path
    path('register/', RegisterView.as_view(), name='register'),
    path('api-token-auth/', drf_views.obtain_auth_token),
    path('', include(router.urls)),  # Event endpoints
]
