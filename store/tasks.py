from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.db import transaction

from .models import Store
from user.models import Profile


@shared_task
def buy(username, pk):
    with transaction.atomic():
        user = Profile.objects.select_for_update().filter(username=username)[0]
        store = Store.objects.select_for_update().filter(pk=pk).prefetch_related('special_users')[0]
        if user not in store.special_users.all() and user.budget >= store.price:
            user.budget = user.budget - store.price
            store.special_users.add(user)
            user.save()
            store.save()
