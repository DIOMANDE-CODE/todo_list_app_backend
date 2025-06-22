from django.db import models
from account.models import Utilisateur

# Create your models here.


# Modèle des taches groupées

class TaskGroup(models.Model):
    titre_groupe = models.CharField(max_length=200)
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="proprietaire_liste")
    collaborateurs = models.ManyToManyField(Utilisateur, blank=True, related_name='shared_list')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre_groupe
    

# Modèle de la tache

class Task(models.Model):
    groupe_tache = models.ForeignKey(TaskGroup, related_name="taches", on_delete=models.CASCADE, blank=True)
    titre_tache = models.CharField(max_length=200)
    description_tache = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    delai_tache = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre_tache

