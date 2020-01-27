from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


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


class Signup(APIView):

    def post(self, request):
        print(request.data.get('username'))
        user, _ = User.objects.get_or_create(username=request.data.get('username'))
        user.set_password(request.data.get('password'))
        user.save()
        profile, _ = Profile.objects.get_or_create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        return HttpResponse('ok')
