from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedModelSerializer

from .models import Profile


class ProfileSerializer(HyperlinkedModelSerializer):
    username = SerializerMethodField()

    def get_username(self, profile):
        return profile.user.username

    class Mata:
        model = Profile
        fields = ('username', 'full_name')


class ProfileDetailsSerializer(ModelSerializer):
    username = SerializerMethodField()
    email = SerializerMethodField()

    def get_username(self, profile):
        return profile.user.username

    def get_email(self, profile):
        return profile.user.email

    class Meta:
        model = Profile
        fields = ('username',
                  'full_name',
                  'email',
                  'birth_date',
                  'phone',
                  'national_code',
                  'field_study',
                  'grade',
                  'marks',
                  )
