from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sports_interested = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    SPORT_CHOICES = [
        ('Football', 'Football'),
        ('Cricket', 'Cricket'),
        ('Badminton', 'Badminton'),
        ('Basketball', 'Basketball'),
        ('Tennis', 'Tennis'),
        ('Volleyball', 'Volleyball'),
        ('Table Tennis', 'Table Tennis'),
        ('Running', 'Running'),
    ]

    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=100)
    total_players = models.PositiveIntegerField()
    event_description = models.TextField(blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return self.event_name


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} joined {self.event.event_name}"

class EventJoinInfo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.full_name} - {self.event.event_name}"
