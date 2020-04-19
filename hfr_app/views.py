from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from hfr_app.models import Feeder, Schedule
from hfr_app.serializers import UserSerializer, FeederSerializer, ScheduleSerializer


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
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        feeder = self.kwargs['pk']
        return Schedule.objects.filter(feeder=feeder)


class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        feeder = self.kwargs['pk']
        return Schedule.objects.filter(feeder=feeder)
