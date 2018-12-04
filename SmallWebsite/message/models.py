from django.urls import reverse
from django.db import models
from user.models import UserRegister


# Create your models here.
class new_messages(models.Model):
    NEW_KINDS = (
        ('A','新闻'),
        ('B','政策'),
        ('C','行情'),
        ('D','技术'),
        ('E','快讯')
    )
    new_title = models.CharField(max_length=200,null=False)
    new_type = models.CharField(max_length=1,choices=NEW_KINDS,null=False)
    new_detail = models.TextField(max_length=20000,null=False)
    new_img = models.ImageField(upload_to='images/cover')
    new_source = models.CharField(max_length=200)
    new_pub = models.DateTimeField(auto_now=True)
    new_auth = models.CharField(max_length=100)
    to_count = models.IntegerField(default=0)
    look_count = models.IntegerField(default=0)
    thumbup_count = models.IntegerField(default=0)
    exmstatus = models.CharField(max_length=10,default="待审核")
    thumbup_user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='thumbup')
    pub_user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='pubuser')

    def get_url_path(self):
        return reverse("message:detail", args=[self.new_type, self.id])