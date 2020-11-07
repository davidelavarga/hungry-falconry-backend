from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from hfr_app.models import Feeder, Schedule, Hub


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class FeederSerializer(ModelSerializer):
    class Meta:
        model = Feeder
        fields = '__all__'


class HubSerializer(ModelSerializer):
    class Meta:
        model = Hub
        fields = '__all__'


class UserSerializer(HyperlinkedModelSerializer):
    hubs = HubSerializer(many=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'hubs']


# Get all data
class RecursiveFeederSerializer(ModelSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = Feeder
        fields = '__all__'


class AllHubDataSerializer(ModelSerializer):
    feeders = RecursiveFeederSerializer(many=True)

    class Meta:
        model = Hub
        fields = '__all__'
