from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from hfr_app.models import Feeder, Schedule


class ScheduleSerializer(ModelSerializer):
    slug_scheduler = serializers.ReadOnlyField(source='slug_scheduler')

    class Meta:
        model = Schedule
        fields = '__all__'


class FeederSerializer(ModelSerializer):
    class Meta:
        model = Feeder
        fields = '__all__'


class UserSerializer(HyperlinkedModelSerializer):
    feeders = FeederSerializer(many=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'feeders']
