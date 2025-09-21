from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sports_interested = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    sport_type = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255)
    total_players = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    event_description = models.TextField(blank=True, null=True)

    # This is the required addition to fix the error
    def __str__(self):
        return f"{self.event_name} on {self.event_date}"

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} joined {self.event.event_name}"


class EventJoinInfo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    joined_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} joined {self.event}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


