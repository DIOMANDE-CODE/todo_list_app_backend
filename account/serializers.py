from rest_framework import serializers
from .models import Utilisateur

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta :
        model = Utilisateur
        fields = ['id','account_image','account_email','password','account_name','is_active','is_staff']
        extra_kwargs = {
            'password':{'write_only':True}
        }
        reads_only_fields = ['id', 'account_created', 'account_updated']

    def create(self, validated_data):
        password = validated_data.pop('password')

        if not password:
            raise serializers.ValidationError({"password": "Ce champ est obligatoire."})
        
        user = Utilisateur(**validated_data)
        user.set_password(password)
        user.save()
        return user
    