from django.contrib import admin
from django.urls import path,include
from .views import CreateCalendarAPI

urlpatterns = [
    path('rest/v1/calendar/init/',CreateCalendarAPI.as_view(),name="List of Event"),
]   