from rest_framework import serializers

class MailAuthViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    verificationtoken = serializers.CharField()
    verificationcode= serializers.CharField()
    