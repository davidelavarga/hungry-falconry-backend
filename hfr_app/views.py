from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from hfr_app.models import Feeder, Schedule
from hfr_app.serializers import UserSerializer, FeederSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class FeederList(ListCreateAPIView):
    queryset = Feeder.objects.all()
    serializer_class = FeederSerializer


class FeederDetail(RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a snippet instance.
    """
    queryset = Feeder.objects.all()
    serializer_class = FeederSerializer


class ScheduleList(ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = FeederSerializer


class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a snippet instance.
    """
    queryset = Schedule.objects.all()
    serializer_class = FeederSerializer
    lookup_field = 'slug_scheduler'


