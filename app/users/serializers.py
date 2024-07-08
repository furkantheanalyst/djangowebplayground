from rest_framework import serializers
from .models import User, Message, MailAuth

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','name','email','password']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields=['name','description']

class MailAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model=MailAuth
        fields=['username','temptoken','verifycode','logintime']