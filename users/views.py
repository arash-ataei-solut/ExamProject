from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .serializers import ProfileSerializer, ProfileDetailsSerializer


class ProfileViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializers = {
        'list': ProfileSerializer,
        'retrieve': ProfileDetailsSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)
