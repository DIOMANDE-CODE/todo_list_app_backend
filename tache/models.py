from django.db import models
from account.models import Utilisateur
from django.utils import timezone

# Create your models here.


# Modèle des taches groupées

status = [
    ('à faire','à faire'),
    ('en cours','en cours'),
    ('termine','termine'),
]

class Tache(models.Model):
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="proprietaire_liste")

    nom_tache = models.CharField(max_length=200)
    description_tache = models.TextField(blank=True, null=True)
    status_tache = models.CharField(max_length=10, choices=status, default='à faire')
    echeance_tache = models.DateField(blank=True, null=True, default=timezone.now)
    collaborateurs = models.ManyToManyField(Utilisateur, blank=True, related_name='shared_list')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom_tache
    

# Modèle de la tache

class SousTache(models.Model):
    tache = models.ForeignKey(Tache, related_name="taches", on_delete=models.CASCADE, blank=True)
    nom_sous_tache = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_sous_tache

