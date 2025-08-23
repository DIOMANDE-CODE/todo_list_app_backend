from rest_framework import serializers

class PasswordResetSerializers(serializers.Serializer):
    email = serializers.EmailField()

class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField()