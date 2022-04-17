from django.shortcuts import render,redirect
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import render
from .serializers import EventSerializer  ,   Event
from .utils import connect_to_calendar
from rest_framework.permissions import IsAuthenticated

# Create your views here.



class CreateCalendarAPI(ListCreateAPIView):
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    permission_classes = [IsAuthenticated]

    def GoogleCalendarInitView(self,serializer):
        serializer.save_as(request=self.request)

    def GoogleCalendarRedirectView(self,request):
        context = {"data" : self.GoogleCalendarInitView()}
        return render(request,"eventListing.html",context)    
        