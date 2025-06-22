from rest_framework import serializers
from .models import TaskGroup, Task

from account.serializers import UtilisateurSerializer

class TaskSerializer(serializers.ModelSerializer):
    class Meta :
        model = Task
        fields = '__all__'
        reads_only_fields = ['id','groupe_tache','created_at', 'updated_at']

class TaskGroupSerializer(serializers.ModelSerializer):

    proprietaire = UtilisateurSerializer(required=False, read_only=True)
    collaborateurs = UtilisateurSerializer(required=False, read_only=True, many=True)
    taches = TaskSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = TaskGroup
        fields = '__all__'
        reads_only_fields = ['id','proprietaire','created_at', 'updated_at']