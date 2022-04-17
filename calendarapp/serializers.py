from .models import Event
from django.db.models.query import EmptyQuerySet
#this utils contains all the extra fucntion that we need throughout our project.
from .utils import connect_to_calendar , prepare_event , convert_attendees_to_list

from rest_framework import serializers
from rest_framework.response  import Response
from rest_framework.exceptions import ValidationError



class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['user','organizer','Eid']

    


    def validate(self,data):
        if(data['start_time'] > data['end_time']):
            raise ValidationError("Please enter valid End time,Start time should be before the End time .")
        #qs=Event.objects.filter(user=data['user'])
        return data



    def save_as(self,request):

        #Checking if the user has any another event at the time interval requested . Doing it here because
        #the user was not available before .
        qs=Event.objects.filter(user=request.user)
        q1=qs.filter(start_time__range=(self.data['start_time'],self.data['end_time']))
        q2=qs.filter(end_time__range=(self.data['start_time'],self.data['end_time']))
        q3=qs.filter(start_time__lte=self.data['start_time'],end_time__gte=self.data['end_time'])

        if  q1 or  q2 or q3:
            raise ValidationError(f'You have meetings {self.data["start_time"]} - {self.data["end_time"]}.')
        #This function connects us to google calendar 
        service=connect_to_calendar(request=request)

        #the prepare_event takes the validated_data and provide us the JSOn version to be sent the google calendar
        event=prepare_event(self.validated_data)
        
        #adding event to the google calendar
        
        created_event = service.events().insert(calendarId='primary',sendNotifications=True, body=event).execute()
        #taking the Event id and Organizer from the Calendar Event
        self.validated_data['organizer']=created_event['organizer']['email']
        self.validated_data['Eid']=created_event['id']
        #finally creating our local event
        event=Event.objects.create(user=request.user,**self.validated_data)
        
        return event

