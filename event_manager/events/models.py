from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
#class User(AbstractUser):
 #   email = models.EmailField(unique=True)

class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Event Title")
    description = models.TextField(blank=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, related_name='organized_events', on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_upcoming(self):
        return self.date_time >= timezone.now()

    def __str__(self):
        return self.title