from django.utils import timezone
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Event
from .serializers import EventSerializer, RegisterSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Event Management API!")


User = get_user_model()

# Custom permission to allow only event organizers to edit
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user or request.method in permissions.SAFE_METHODS

# Event viewset with filtering and upcoming events
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

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

# User registration view with event capacity check
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=404)

        current_registrations = event.registrations.count()
        if current_registrations >= event.capacity:
            return Response({"detail": "Event capacity reached."}, status=400)

        return super().create(request, *args, **kwargs)

# List view for upcoming events with filters
class EventListView(generics.ListAPIView):
    queryset = Event.objects.filter(date_time__gte=timezone.now())
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'title': ['icontains'],
        'location': ['icontains'],
        'date_time': ['gte', 'lte'],
    }
