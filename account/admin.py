from django.contrib import admin
from .models import Utilisateur

# Register your models here.

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('account_email','account_image','account_name','account_created','account_updated','is_active','is_staff',)
    search_fields = ('account_name',)
    ordering = ['account_name']
