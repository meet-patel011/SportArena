from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import EventForm, RegisterForm, LoginForm, EventJoinForm
from .models import Event, UserProfile, EventParticipant, EventJoinInfo
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q 

# Home Page View
def home(request):
    # Show 3 upcoming events as featured
    featured_events = Event.objects.filter(event_date__gte=date.today()).order_by('event_date')[:3]
    return render(request, 'events/index.html', {'featured_events': featured_events})


# Events List Page View
def events(request):
    # Auto-delete past events
    Event.objects.filter(event_date__lt=date.today()).delete()

    query = request.GET.get('q')  # Get the search query

    if query:
        all_events = Event.objects.filter(
            Q(event_name__icontains=query) | Q(event_location__icontains=query)
        ).order_by("event_date")
    else:
        all_events = Event.objects.all().order_by("event_date")

    return render(request, 'events/events.html', {"events": all_events})


# Add New Event (only accessible by logged-in users)
@login_required
def add_events(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Link event to the logged-in organizer
            event.save()
            return redirect('/events/?message=Event added successfully!')
    else:
        form = EventForm()

    return render(request, 'events/add_events.html', {"form": form})


# Contact Page View
def contact(request):
    return render(request, 'events/contact.html')


# User Registration View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            sports = form.cleaned_data.get('sports_interested')
            city = form.cleaned_data.get('city')
            # Create UserProfile with additional fields
            UserProfile.objects.create(user=user, sports_interested=sports, city=city)
            return redirect('/user_login/?message=Account created successfully! Please log in.')
    else:
        form = RegisterForm()

    return render(request, 'events/register.html', {'form': form})


# User Login View
def user_login(request):
    message = request.GET.get('message')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/?message=Logged in successfully!')
    else:
        form = LoginForm()

    return render(request, 'events/user_login.html', {'form': form, 'message': message})


# Join Event View (only accessible by logged-in users)
@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    already_joined = EventParticipant.objects.filter(event=event, user=request.user).exists()
    if already_joined:
        return redirect('/events/?message=You have already joined this event.')
    
    participants_count = EventParticipant.objects.filter(event=event).count()
    if participants_count >= event.total_players:
        return redirect('/events/?message=Event is full. Cannot join.')

    if request.method == "POST":
        form = EventJoinForm(request.POST)
        if form.is_valid():
            # Save the additional join information
            join_info = form.save(commit=False)
            join_info.event = event
            join_info.user = request.user
            join_info.save()

            # Add the user as a participant
            EventParticipant.objects.create(event=event, user=request.user)

            return redirect(f'/events/?message=You successfully joined the event: {event.event_name}')
    else:
        form = EventJoinForm()

    return render(request, 'events/join_event.html', {'form': form, 'event': event})


# Shows events created by logged-in user
@login_required
def my_events(request):
    my_created_events = Event.objects.filter(organizer=request.user).order_by("event_date")
    return render(request, 'events/my_events.html', {"events": my_created_events})

# edit and delete created events
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure only organizer can edit
    if event.organizer != request.user:
        return redirect('/my_events/?message=You are not allowed to edit this event.')

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('/my_events/?message=Event updated successfully!')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {"form": form})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure only organizer can delete
    if event.organizer != request.user:
        return redirect('/my_events/?message=You are not allowed to delete this event.')

    if request.method == "POST":
        event.delete()
        return redirect('/my_events/?message=Event deleted successfully!')
    
    # Show confirmation page
    return render(request, 'events/delete_event.html', {"event": event})

# Organizer Dashboard
@login_required
def organizer_dashboard(request):
    # Get all events organized by this user
    my_events = Event.objects.filter(organizer=request.user).order_by("event_date")

    # For each event, get join info
    events_with_participants = []
    for event in my_events:
        join_infos = EventJoinInfo.objects.filter(event=event)
        events_with_participants.append({
            'event': event,
            'join_infos': join_infos
        })

    return render(request, 'events/organizer_dashboard.html', {
        'events_with_participants': events_with_participants
    })
