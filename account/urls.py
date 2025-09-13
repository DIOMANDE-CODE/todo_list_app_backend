from django.urls import path
from .views import  liste_utilisateur, delete_all_tokens, detail_utilisateur,register,login,logout,activer_compte

urlpatterns = [
    path('', liste_utilisateur, name='liste_utilisateur'),
    path('info/', detail_utilisateur, name='detail_utilisateur'),
    path('delete/tokens/', delete_all_tokens, name='delete_all_token'),

    # urls token pour connexion et deconnexion
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    # url pour activer un compte
    path('activation/<int:uid>/<str:token>/', activer_compte, name='activer_compte'),
]