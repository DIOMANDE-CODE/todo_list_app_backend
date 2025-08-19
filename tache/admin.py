from django.contrib import admin
from .models import Tache, SousTache

# Register your models here.

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('nom_tache', 'description_tache', 'status_tache', 'echeance_tache','proprietaire','created_at', 'updated_at',)
    search_fields = ('nom_tache',)
    ordering = ['nom_tache']


@admin.register(SousTache)
class SousTacheAdmin(admin.ModelAdmin):
    list_display = ('nom_sous_tache', 'is_completed', 'created_at', 'updated_at',)
    search_fields = ('nom_sous_tache',)
    ordering = ['nom_sous_tache']