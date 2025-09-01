from django.urls import path
from .views import liste_tache, create_tache, detail_tache, create_sous_tache, detail_sous_tache, ajout_collaborateurs, suppression_collaborateurs, search_tache

urlpatterns = [

    # urls Tache
    path('list/', liste_tache, name='liste_tache'),
    path('create/', create_tache, name='create_tache'),
    path('detail/<int:pk>/', detail_tache, name='detail_tache'),

    # urls Sous Tache
    path('<int:tache_id>/sous_tache/create/', create_sous_tache, name='create_sous_tache'),
    path('<int:sous_tache_id>/sous_tache/detail/', detail_sous_tache, name='detail_sous_tache'),

    # urls ajout_collaborateurs
    path('<int:tache_id>/ajout/collaborateur/', ajout_collaborateurs, name='ajout_collaborateur'),

    # urls suppression_collaborateurs
    path('<int:pk>/suppression/collaborateur/<str:email_collaborateur>/', suppression_collaborateurs, name='suppression_collaborateurs'),

    # urls recherche de tache
    path('', search_tache, name='search_tache'),
]