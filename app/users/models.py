from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=256, unique=True)
    name=models.CharField(max_length=256)
    email=models.CharField(max_length=256, unique=True)
    password=models.CharField(max_length=256)
    
    REQUIRED_FIELDS=[]

class Message(models.Model):
    name=models.CharField(max_length=64)
    description=models.CharField(max_length=256)

    def __str__(self):
        return self.name

class MailAuth(models.Model):
    username=models.CharField(max_length=256)
    temptoken=models.CharField(max_length=256, unique=True)
    verifycode=models.CharField(max_length=6)
    logintime=models.DateTimeField(auto_now=True)