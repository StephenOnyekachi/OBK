from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_otp.oath import TOTP
from django_otp.util import random_hex


# Create your models here.

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance= None, created=False, **kwargs):
#     if created:
#         Users.objects.create(user=instance)

class Users(AbstractUser):
    currency = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=200)
    address = models.CharField(max_length=250)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    balance = models.FloatField(default=0.00, null=True)
    account_number = models.PositiveIntegerField(default=0, null=True)
    account_type = models.CharField(max_length=200)
    bank = models.CharField(max_length=200)
    block = models.BooleanField(default=False)
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='picture')

    def __str__(self):
        return self.username
    
class Transfer_otp(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='otp_for_sender')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='otp_for')
    account = models.IntegerField(default=12)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    amount = models.FloatField(default=0.00, null=True)
    time_stamp = models.DateTimeField(verbose_name="time", auto_now=True)

    def __str__(self):
        return self.user.username
    
class OTP(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_otp')
    receiver_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='receivers_otp')
    account = models.IntegerField(default=12)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    amount = models.FloatField(default=0.00, null=True)
    time_stamp = models.DateTimeField(verbose_name="time", auto_now=True)

    def __str__(self):
        return self.user.username

class Transactions(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='receiver')
    amount = models.PositiveIntegerField(default=0.00)
    time_stamp = models.DateTimeField(verbose_name="time stamp", auto_now=True)
    otp = models.PositiveIntegerField()
    reffrence_code = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __int__(self):
        return self.amount
