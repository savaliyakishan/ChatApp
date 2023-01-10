from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profileImages = models.ImageField(upload_to='images',default="defultprofile.png",db_column="User_Img")
    phoneNumber = models.BigIntegerField(db_column="User_PhoneNumber")
    gender = models.CharField(max_length=255,db_column="Gender")

