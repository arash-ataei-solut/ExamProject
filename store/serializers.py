from rest_framework import serializers

from .models import Store
from user.serializers import ProfileSerializer


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        fields = ['url', 'title', 'num_chasers']


class StoreDetailSerializer(serializers.ModelSerializer):
    owners = ProfileSerializer(many=True)

    class Meta:
        model = Store
        fields = ['owners', 'title', 'about', 'chasers', 'num_chasers', 'price']
