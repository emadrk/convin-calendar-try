from datetime import datetime
from allauth.socialaccount.models import SocialAccount,SocialToken
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.contrib.auth.models import User
from django.shortcuts import render




def time_available(self,request,d1,d2):
    pass

#Connect to Google Calendar
def connect_to_calendar(request):
    #Fetches the User of the request
    qs=SocialAccount.objects.filter(user=request.user)
    print(request.user)
    #Fetches the Access token of the User
    token=SocialToken.objects.filter(account=qs[0]).values('token')

    #The scope of service like if we want readonly etc
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    #Finally making a connection request
    creds = Credentials(token[0]['token'],SCOPES )
    service = build('calendar', 'v3', credentials=creds)
    return service




#This function accept comma separated string of email like "emadk3@gmail.com , zyx@gmail.com " 
# and returns a list of dictionary in the format : [ {'email' : 'emadk3@gmail.com'} , {'email' : 'zyx@gmail.com' }]
def convert_attendees_to_list(attendees):
        res=list()
        for i in attendees.split(','):
            d=dict()
            d['email']=i.strip()
            res.append(d)
        return res






#This function convert date into 2021-03-22T00:40:00+05:30
def convert_RFC(date):
    return str(date.isoformat('T'))
    



# This function gives event which we are using to render on html, the data retured by this function is handled by GoogleCalendarRedirectView method in views.py file.
def prepare_event(data):
    start=convert_RFC(data["start_time"])
    end=convert_RFC(data["end_time"])
    email=convert_attendees_to_list(data['attendees'])
    event = {
        'summary': data["summary"],
        'description': data["description"],
        'start': {
            'dateTime': start,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': email,
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        }
    }
    return event
    
