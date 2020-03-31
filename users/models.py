from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db import models
from datetime import time

from .managers import CustomUserManager
from .utils import random_code
from .choices import *

import datetime

class Person(AbstractUser):
    username = None
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(_('Email Address'), unique=True, null=True)
    code = models.CharField(max_length=28, null=True, default=random_code)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
                return f'{self.name}_{self.last_name}'

class Token(models.Model):
    token = models.CharField(max_length=300)
    user = models.OneToOneField(Person, on_delete=models.CASCADE)
    
    def __str__(self):
            return f'{self.user.email}_token'

class Day(models.Model):
    day = models.CharField(max_length=9)
    number = models.IntegerField()

    def __str__(self):
        return f'{self.day}'

class GymAccount(models.Model):
    age = models.IntegerField(null=True, validators=[MinValueValidator(10), MaxValueValidator(100)])
    sport_field = models.CharField(max_length=12, choices=Sport_Field, null=True)
    days_of_week = models.ManyToManyField(Day)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    user = models.OneToOneField(Person, on_delete=models.CASCADE)

    class Meta:
        abstract = True

# Coach class
class Coach(GymAccount):
    salary = models.BigIntegerField(default = 1500000)

    def __str__(self):
        return f'{self.user.name}_{self.user.last_name}'

# Athlete class
class Athlete(GymAccount):
    last_payment = models.DateField(default=now, blank=True)
    trainer = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, blank=True,
    related_name='user_trainer')

    def __str__(self):
        return f'{self.user.name}_{self.user.last_name}'

class FinancialTradeOff(models.Model):
    details = models.CharField(max_length=250, null=True)
    date = models.DateTimeField(default=now)
    amount = models.BigIntegerField(null=True)
    user = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=48, default=random_code)

    class Meta:
        abstract = True

class Income(FinancialTradeOff):
    def __str__(self):
        return f'{self.user} {self.date} {self.amount} toman'

class Expense(FinancialTradeOff):
    def __str__(self):
        return f'{self.user} {self.date} {self.amount} toman'