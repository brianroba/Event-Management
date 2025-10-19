from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserRegisterView, EventRegisterView, home
from rest_framework.authtoken import views as drf_views

router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')

urlpatterns = [
    path('', home, name='home'),  # Root path
    path('register/', UserRegisterView.as_view(), name='user-register'),  #for user sign-up
    path('event-register/', EventRegisterView.as_view(), name='event-register'),  #for event signup
    path('api-token-auth/', drf_views.obtain_auth_token),
    path('events/', include(router.urls)),  # Event endpoints
]
