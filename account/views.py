from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError 
from django.http import JsonResponse

from .models import Utilisateur
from .serializers import UtilisateurSerializer


# Create your views here.

# Page acceuil
def acceuil(request):
    return JsonResponse({
        'message':'Bienvenue sur ma todo app'
    })

# Fonction de deconnexion : logout
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # met le token dans la blacklist
            return Response({"detail": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Le champ 'refresh' est requis."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Token invalide ou déjà blacklisté."}, status=status.HTTP_400_BAD_REQUEST)

# Creation d'un utilisateur : POST
@api_view(['POST'])
def creation_utilisateur(request):
    serializer = UtilisateurSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message':'Utilisateur crée avec succès',
            'utilisateur':serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lister les utilisateur inscrits
@api_view(['GET'])
def liste_utilisateur(request):
    utilisateurs = Utilisateur.objects.all()
    serializer = UtilisateurSerializer(utilisateurs, many=True)
    return Response(serializer.data)