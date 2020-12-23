from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from hexagonal_settings import get_settings
from hfr_app.models import Feeder, Schedule, Hub
from hfr_app.serializers import UserSerializer, FeederSerializer, ScheduleSerializer, HubSerializer, \
    AllHubDataSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class HubList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HubSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Hub.objects.all()
        return Hub.objects.filter(owner=self.request.user)


class HubDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = HubSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Hub.objects.all()
        return Hub.objects.filter(owner=self.request.user)


class FeederList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeederSerializer

    def get_queryset(self):
        hub = self.kwargs['pk']
        return Feeder.objects.filter(hub=hub)


class FeederDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = FeederSerializer
    lookup_field = 'id'

    def get_queryset(self):
        hub = self.kwargs['pk']
        return Feeder.objects.filter(hub=hub)


class ScheduleList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        """
        Return a list of schedules based on feeder id
        """
        feeder = self.kwargs['pk2']
        return Schedule.objects.filter(feeder=feeder)

    def post(self, request, *args, **kwargs):
        """
        Send request to feeder device and save it
        :return: Scheduled created
        """
        try:
            # Get MAC
            hub_id = self.kwargs["pk"]
            feeder_id = self.kwargs['pk2']
            hub = Feeder.objects.get(id=feeder_id, hub=hub_id).hub
            # Create schedule object and save it in database
            schedule = self.create(request, *args, **kwargs)
            # Once the schedule is created, send it to feeder device
            get_settings().feeder_communication().publish_schedule_request(schedule.data, "add", hub.mac_address,
                                                                           feeder_id)
            return schedule
        except Exception as e:
            # TODO: Removed schedule when something fails
            print(f"Should remove schedule: {e}")


class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ScheduleSerializer
    lookup_field = 'id'

    def get_queryset(self):
        feeder = self.kwargs['pk2']
        return Schedule.objects.filter(feeder=feeder)

    def delete(self, request, *args, **kwargs):
        try:
            # Get MAC
            hub_id = self.kwargs["pk"]
            feeder_id = self.kwargs['pk2']
            schedule_id = self.kwargs['id']
            hub = Feeder.objects.get(id=feeder_id, hub=hub_id).hub
            # Send to remove it in the hub
            get_settings().feeder_communication().publish_schedule_request({"id": schedule_id}, "remove",
                                                                           hub.mac_address, feeder_id)
            # Finally remove it from the DB
            schedule = self.destroy(request, *args, **kwargs)
            return schedule
        except Exception as e:
            # TODO: Removed schedule when something fails
            print(f"Cannot remove schedule: {e}")


class HubData(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AllHubDataSerializer

    def get_queryset(self):
        hub = self.kwargs['pk']
        return Hub.objects.filter(id=hub)
