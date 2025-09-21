from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import EventForm, RegisterForm, LoginForm, EventJoinForm, ContactForm
from .models import Event, UserProfile, EventParticipant, EventJoinInfo, ContactMessage
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q 
from django.core.mail import send_mail
from django.conf import settings

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

# Contact page view
def contact(request):
    message_info = ''
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save in DB (optional)
            form.save()

            # Send Email to Admin
            send_mail(
                subject=f'New Contact from {form.cleaned_data["name"]}',
                message=f"""
                Name: {form.cleaned_data["name"]}
                Email: {form.cleaned_data["email"]}
                Message:
                {form.cleaned_data["message"]}
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['admin@example.com'],  # Change to your admin email
                fail_silently=False,
            )

            message_info = "Thank you! Your message has been sent successfully."
            return redirect(f'/contact/?message={message_info}')
    else:
        form = ContactForm()

    message_info = request.GET.get('message', '')

    return render(request, 'events/contact.html', {
        'form': form,
        'message': message_info,
    })


# User Registration View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            sports = form.cleaned_data.get('sports_interested')
            city = form.cleaned_data.get('city')

            # Create UserProfile manually
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

# Join event view
@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Prevent joining multiple times
    already_joined = EventParticipant.objects.filter(event=event, user=request.user).exists()
    if already_joined:
        return redirect('/events/?message=You have already joined this event.')

    # Prevent joining if event is full
    participants_count = EventParticipant.objects.filter(event=event).count()
    if participants_count >= event.total_players:
        return redirect('/events/?message=Event is full. Cannot join.')

    if request.method == "POST":
        form = EventJoinForm(request.POST)
        if form.is_valid():
            # Match email in form with logged-in user's email
            input_email = form.cleaned_data.get('email')
            if input_email != request.user.email:
                form.add_error('email', "Email must match your registered email.")
            else:
                # Save the join info separately
                join_info = EventJoinInfo.objects.create(
                    event=event,
                    user=request.user,
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number']
                )

                # Add the user as a participant
                EventParticipant.objects.create(event=event, user=request.user)

                return redirect(f'/events/?message=Successfully joined the event: {event.event_name}')
    else:
        form = EventJoinForm(initial={'email': request.user.email})

    return render(request, 'events/join_event.html', {
        'form': form,
        'event': event
    })


# edit and delete created events
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure only organizer can edit
    if event.organizer != request.user:
        return redirect('/dashboard/?message=You are not allowed to edit this event.')

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/?message=Event updated successfully!')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {"form": form})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure only organizer can delete
    if event.organizer != request.user:
        return redirect('/dashboard/?message=You are not allowed to delete this event.')

    if request.method == "POST":
        event.delete()
        return redirect('/dashboard/?message=Event deleted successfully!')
    
    # Show confirmation page
    return render(request, 'events/delete_event.html', {"event": event})


@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None  

    created_events = Event.objects.filter(organizer=request.user)
    joined_events = EventParticipant.objects.filter(user=request.user)

    for event in created_events:
        sport_slug = event.sport_type.lower().replace(' ', '')
        event.image_path = f'events/images/{sport_slug}.jpg'

        # Get participant + join info
        participants = EventParticipant.objects.filter(event=event).select_related('user')
        event.participant_details = []
        for p in participants:
            join_info = EventJoinInfo.objects.filter(event=event, user=p.user).first()
            event.participant_details.append({
                "username": p.user.username,
                "email": p.user.email,
                "name": join_info.name if join_info else "-",
                "phone": join_info.phone_number if join_info else "-",
            })


    for joined in joined_events:
        sport_slug = joined.event.sport_type.lower().replace(' ', '')
        joined.image_path = f'events/images/{sport_slug}.jpg'

    return render(request, 'events/dashboard.html', {
        'profile': profile,
        'created_events': created_events,
        'joined_events': joined_events,
    })


@login_required
def cancel_joined_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participation = EventParticipant.objects.filter(event=event, user=request.user)

    if participation.exists():
        participation.delete()
        message = f'You have successfully cancelled your participation in: {event.event_name}.'
    else:
        message = 'You are not a participant of this event.'

    return redirect(f'/dashboard/?message={message}')

def contact(request):
    success_message = None

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            success_message = "Your message has been sent successfully!"

    return render(request, 'events/contact.html', {
        'success_message': success_message
    })

