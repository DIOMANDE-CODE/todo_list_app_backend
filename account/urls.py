from django.urls import path
from .views import creation_utilisateur, liste_utilisateur

urlpatterns = [
    path('create/', creation_utilisateur, name='create_utilisateur'),
    path('', liste_utilisateur, name='liste_utilisateur'),

    
]
