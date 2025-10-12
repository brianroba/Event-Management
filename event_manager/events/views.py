from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Q
from .models import Event
from .serializers import EventSerializer
from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import Count

# Create your views here.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user or request.method in permissions.SAFE_METHODS

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Event.objects.all()

        if self.action == 'upcoming':
            queryset = queryset.filter(date_time__gte=timezone.now())

        title = self.request.query_params.get('title')
        location = self.request.query_params.get('location')
        date_from = self.request.query_params.get('from')
        date_to = self.request.query_params.get('to')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if date_from and date_to:
            queryset = queryset.filter(date_time__range=[date_from, date_to])

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        upcoming_events = self.get_queryset().filter(date_time__gte=timezone.now())
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)
 

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    event = Event.objects.get(pk=event_id)
    current_registrations = event.registrations.count()  # Assuming related name 'registrations'
    if current_registrations >= event.capacity:
        return Response({"detail": "Event capacity reached."}, status=400)
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class EventListView(generics.ListAPIView):
    queryset = Event.objects.filter(date__gte=timezone.now())  # Upcoming events
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'title': ['icontains'],       # Case-insensitive contains
        'location': ['icontains'],
        'date': ['gte', 'lte'],       # Date range filtering
    }

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # prevent duplicate registrations

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # prevent duplicate registrations

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated