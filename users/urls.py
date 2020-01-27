from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ProfileViewSet, Signup


router = SimpleRouter()

router.register('profile', ProfileViewSet)


urlpatterns = [
    path('signup/', Signup)
]
