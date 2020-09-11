from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView

from hfr_app.models import Feeder, Schedule
from hfr_app.serializers import UserSerializer, FeederSerializer, ScheduleSerializer

from config import get_settings

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


class FeederList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeederSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Feeder.objects.all()
        return Feeder.objects.filter(owner=self.request.user)


class FeederDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = FeederSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Feeder.objects.all()
        return Feeder.objects.filter(owner=self.request.user)


class ScheduleList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        """
        Return a list of schedules based on feeder id
        """
        feeder = self.kwargs['pk']
        return Schedule.objects.filter(feeder=feeder)

    def post(self, request, *args, **kwargs):
        """
        Send request to feeder device and save it
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # TODO async???
        schedule = self.create(request, *args, **kwargs)
        get_settings().feeder_communication().publish_schedule_request(schedule.data, self.request.user.auth_token.key)
        return self.create(request, *args, **kwargs)


class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ScheduleSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        """
        feeder = self.kwargs['pk']
        return Schedule.objects.filter(feeder=feeder)
