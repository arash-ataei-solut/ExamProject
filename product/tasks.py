from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.db import transaction

from .models import Product, Rate, MediaFile
from user.models import Profile


@shared_task
def rate(username, pk, rate_num):
    user = Profile.objects.get(username=username)
    if user:
        product = Product.objects.get(pk=pk)
        rate_obj, _ = Rate.objects.get_or_create(user=user, product=product)
        rate_obj.rate = rate_num
        rate_obj.save()


@shared_task
def buy(username, pk):
    with transaction.atomic():
        user = Profile.objects.select_for_update().filter(username=username)[0]
        product = Product.objects.select_for_update().filter(pk=pk).prefetch_related('special_users')[0]
        if user not in product.special_users.all() and user.budget >= product.price:
            user.budget = user.budget - product.price
            product.special_users.add(user)
            user.save()
            product.save()


@shared_task
def buy_media(username, pk):
    with transaction.atomic():
        user = Profile.objects.select_for_update().filter(username=username)[0]
        media = MediaFile.objects.select_for_update().filter(pk=pk).prefetch_related('special_users')[0]
        if user not in media.special_users.all() and user.budget >= media.price:
            user.budget = user.budget - media.price
            media.special_users.add(user)
            user.save()
            media.save()
