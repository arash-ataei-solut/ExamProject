from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from examMaker.models import Exam


def is_national_code(value):
    if value.isdigit() and len(value) == 10:
        return value
    else:
        return ValidationError(_('%(value)s is not valid national code'), params={'value': value})


def is_phone(value):
    if value.isdigit() and value.startswith('09') and len(value) == 11:
        return value
    else:
        return ValidationError(_('%(value)s is not valid phone number'), params={'value': value})


class Profile(models.Model):
    GRADE_CHOICES = [
        ('U', 'Undergraduate'),
        ('M', 'Masters Degree'),
        ('P', 'PHD'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', related_query_name='profile')
    birth_date = models.DateField()
    phone = models.CharField(max_length=11, validators=[is_phone, ])
    national_code = models.CharField(max_length=10, validators=[is_national_code, ])
    field_study = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)

    @property
    def first_name(self):
        user = User.objects.get(profile=self)
        return user.first_name

    @property
    def last_name(self):
        user = User.objects.get(profile=self)
        return user.last_name

    @property
    def full_name(self):
        return str(self.first_name) + str(self.last_name)

    def __str__(self):
        return self.full_name


class Marks(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='marks', related_query_name='mark')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    mark = models.DecimalField(max_digits=2, decimal_places=2)

