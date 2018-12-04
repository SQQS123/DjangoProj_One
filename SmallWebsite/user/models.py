from django.db import models


# Create your models here.
class UserRegister(models.Model):
    account_number = models.CharField(max_length=11,unique=True)
    password = models.CharField(max_length=200)
    level = models.IntegerField(default=0)
    scores = models.IntegerField(default=0)
    portrait = models.ImageField(default='portrait/')
    mini_name = models.CharField(max_length=50)
    times = models.IntegerField(default=0)
