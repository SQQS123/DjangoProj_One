from django.db import models

# Create your models here.
from user.models import UserRegister


class Charge(models.Model):
    intg_num = models.IntegerField()
    intg_detail = models.CharField(max_length=100)
    use_time = models.TimeField(auto_now=True)


class ChargeRecord(models.Model):
    charge_kind = models.IntegerField()
    charge_time = models.TimeField(auto_now=True)


class NotifyRecord(models.Model):
    comment = models.CharField(max_length=500)
    comment_time = models.TimeField(auto_now=True)
    comment_user = models.ForeignKey(UserRegister,on_delete=models.CASCADE,related_name='comment_user')