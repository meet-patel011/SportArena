from django.contrib import admin
from .models import UserProfile
from .models import Event

admin.site.register(UserProfile)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_name", "sport_type", "event_date", "event_time", "event_location", "total_players")
    search_fields = ("event_name", "sport_type", "event_location")
    list_filter = ("sport_type", "event_date")
