from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CategoryView, SubcategoryView, ProductView, media_buy

router = SimpleRouter()

router.register('category', CategoryView)
router.register('subcategory', SubcategoryView)
router.register('product', ProductView)


urlpatterns = [
    path('media-buy/<int:product_id>/<int:media_id>', media_buy)
] + router.urls
