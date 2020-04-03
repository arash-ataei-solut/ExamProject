from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import StoreView

router = SimpleRouter()

router.register('store', StoreView)


urlpatterns = [

] + router.urls
