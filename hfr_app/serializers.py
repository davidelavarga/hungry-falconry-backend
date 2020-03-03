from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from hfr_app.models import Feeder


class FeederSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Feeder
        fields = '__all__'


class UserSerializer(HyperlinkedModelSerializer):
    feeders = FeederSerializer(many=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'feeders']
