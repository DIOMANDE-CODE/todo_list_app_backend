from django.contrib import admin
from .models import TaskGroup, Task

# Register your models here.

@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ('titre_groupe', 'proprietaire','created_at', 'updated_at',)
    search_fields = ('titre_groupe',)
    ordering = ['titre_groupe']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('titre_tache','groupe_tache',  'description_tache', 'is_completed', 'delai_tache', 'created_at', 'updated_at',)
    search_fields = ('titre_tache',)
    ordering = ['titre_tache']