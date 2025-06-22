from django.urls import path
from .views import liste_groupe_tache, create_groupe_tache, detail_groupe_tache, create_tache, detail_tache, ajout_collaborateurs

urlpatterns = [

    # urls TaskGroup
    path('group/list/', liste_groupe_tache, name='liste_groupe_tache'),
    path('group/create/', create_groupe_tache, name='create_groupe_tache'),
    path('group/detail/<int:pk>/', detail_groupe_tache, name='detail_groupe_tache'),

    # urls Task
    path('<int:groupe_tache_id>/create/', create_tache, name='create_tache'),
    path('<int:tache_id>/detail/', detail_tache, name='detail_tache'),

    # urls ajout_collaborateurs
    path('group/<int:groupe_id>/ajoutcollaborateur/', ajout_collaborateurs, name='ajout_collaborateurs'),
]
