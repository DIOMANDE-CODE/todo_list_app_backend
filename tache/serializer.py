from rest_framework import serializers
from .models import Tache, SousTache

from account.serializers import UtilisateurSerializer


class SousTacheSerializer(serializers.ModelSerializer):

    class Meta:
        model = SousTache
        fields = '__all__'
        reads_only_fields = ['id',  'created_at', 'updated_at', 'proprietaire']


class TacheSerializer(serializers.ModelSerializer):

    proprietaire = UtilisateurSerializer(required=False, read_only=True)
    collaborateurs = UtilisateurSerializer(required=False, read_only=True, many=True)
    taches = SousTacheSerializer(required=False, read_only=True, many=True)

    class Meta :
        model = Tache
        fields = '__all__'
        reads_only_fields = ['id','created_at', 'updated_at', 'proprietaire']