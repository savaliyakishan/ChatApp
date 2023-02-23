from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone


class User(AbstractUser):
    profileImages = models.ImageField(upload_to='images',default="defultprofile.png",db_column="User_Img")
    phoneNumber = models.BigIntegerField(db_column="User_PhoneNumber")
    gender = models.CharField(max_length=255,db_column="Gender")
    active_user = models.BooleanField(default=False,db_column="Active_User")


class messageInfo(models.Model):
    senderUserInfo = models.BigIntegerField(blank=False,null=False,db_column="Sender_Info")
    reciveUserInfo = models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=False,null=False,db_column="Recive_Info")
    message = models.CharField(max_length=99989,blank=False,null=False,db_column="Message_Info")
    sendTime = models.DateTimeField(default=django.utils.timezone.now,db_column="Sending_Time")
    seenStatus = models.BooleanField(default=False,db_column="Seen_Status")