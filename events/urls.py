from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('add_events/', views.add_events, name='add_events'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('join_event/<int:event_id>/', views.join_event, name='join_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cancel_joined_event/<int:event_id>/', views.cancel_joined_event, name='cancel_joined_event'),
]
