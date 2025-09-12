from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Event, EventJoinInfo

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

class EventForm(forms.ModelForm):  
    sport_type = forms.ChoiceField(choices=SPORT_CHOICES)

    class Meta:
        model = Event
        fields = [
            'sport_type',
            'event_name',
            'event_date',
            'event_time',
            'event_location',
            'total_players',
            'event_description',
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'event_description': forms.Textarea(attrs={'rows': 4}),
        }

    # We exclude 'organizer' from the form fields since it will be assigned automatically in views

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    sports_interested = forms.ChoiceField(
        choices=SPORT_CHOICES,
        widget=forms.Select,
        required=True,
        label='Sports Interested In'
    )
    city = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Remove default help texts
        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'label1',
        'placeholder': 'Enter username',
        'required': 'required'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'label1',
        'placeholder': '********',
        'required': 'required'
    }))

class EventJoinForm(forms.ModelForm):
    class Meta:
        model = EventJoinInfo
        fields = ['full_name', 'mobile_number', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Your mobile number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
        }
