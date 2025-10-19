from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EventViewSet
from rest_framework.authtoken import views as drf_views
from .views import RegisterView
from . import views


router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
#   path('auth/', include('rest_framework.urls')),  # Login/logout views
    path('api-token-auth/', drf_views.obtain_auth_token),
    path('register/', RegisterView.as_view(), name='register'),
    path('', views.home, name='home'),

]
