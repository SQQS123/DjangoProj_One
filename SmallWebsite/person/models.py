from django.db import models

# Create your models here.
from user.models import UserRegister
from message.models import new_messages


# 会员购买记录
class Money_Charge_Record(models.Model):
    code = models.CharField(max_length=20)
    charge_money = models.IntegerField()
    charge_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserRegister,on_delete=models.CASCADE,related_name="spend_money_user")


# 我写的积分账单
class Exchange_Record(models.Model):
    # 记录用户干了啥
    detail = models.CharField(max_length=100)
    #  记录积分增加还是减少了多少，有符号
    get_or_cost = models.IntegerField()
    exchange_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserRegister,on_delete=models.CASCADE,related_query_name='exchg_user')


# 积分账单记录
class Charge(models.Model):
    intg_num = models.IntegerField()
    intg_detail = models.CharField(max_length=100)
    use_time = models.TimeField(auto_now=True)


class ChargeRecord(models.Model):
    charge_kind = models.IntegerField()
    charge_time = models.TimeField(auto_now=True)


# 消息通知
class NotifyRec(models.Model):
    comment = models.CharField(max_length=500)
    comment_time = models.TimeField(auto_now=True)
    comment_user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='comment_user')
    commented_message = models.ForeignKey(new_messages, on_delete=models.CASCADE, related_name='commented_message')
