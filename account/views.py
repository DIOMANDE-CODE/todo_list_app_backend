from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


from django.http import JsonResponse

from .models import Utilisateur
from .serializers import UtilisateurSerializer

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken



# Create your views here.

# Page acceuil
def acceuil(request):
    return JsonResponse({
        'message':'Bienvenue sur ma todo app'
    })

# Fonction de connexion avec token généré
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    """
    Connexion avec génération de tokens JWT
    """
    
    email = request.data.get('account_email','').lower().strip()
    password = request.data.get('password','')

    # Verifier l'existence de l'email et le password
    if not email and not password :
        return Response({
            "error":"Email et mot de passe obligatoire"
        },status=status.HTTP_400_BAD_REQUEST)
    
    # Authentification
    user = authenticate(username=email,password=password)

    if not user :
        return Response({
            'error':'Email ou mot de passe incorrect'
        },status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        return Response({
            "error":"Compte désactivé"
        })
    
    # Generation des tokens
    refresh = RefreshToken.for_user(user)

    # Retourner les tokens
    if user is not None :
        return Response({
            "refresh_token":str(refresh),
            "access_token":str(refresh.access_token)
        })
    return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)



# Fonction de deconnexion : logout
@api_view(['POST'])
def logout(request):
    """
    Déconnexion avec blacklist du refresh token
    """

    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist() #Token Invalide

        return Response({"message": "Déconnexion réussie"}, status=205)
    except Exception as e:
        return Response({
            'error': 'Erreur lors de la déconnexion'
        }, status=status.HTTP_400_BAD_REQUEST)
    

# Creation d'un utilisateur : POST
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    # recuperation des données
    email = request.data.get("account_email")
    print(email)

    # Validation de l'addresse Email
    try :
        validate_email(email)
    except ValidationError:
        return Response({
            "error":"Email Invalide"
        }, status=status.HTTP_400_BAD_REQUEST)

    # verifier que l'email est unique
    if Utilisateur.objects.filter(account_email=email).exists():
        return Response({
            "error":"Cet email existe dejà"
        }, status=status.HTTP_400_BAD_REQUEST)
     
    serializer = UtilisateurSerializer(data=request.data)
    if serializer.is_valid():   
        serializer.save()
        return Response({
                'message':'Utilisateur crée avec succès, veuillez vous connecter',
                'utilisateur':serializer.data
            }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# detail/modification d'un compte
@api_view(['GET','PUT'])
def detail_utilisateur(request):

    # Recuperer l'utilisateur connecté
    user = request.user
    
    if request.method == 'GET':
        serializer = UtilisateurSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        serializer = UtilisateurSerializer(user,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lister les utilisateur inscrits
@api_view(['GET'])
@permission_classes([AllowAny])
def liste_utilisateur(request):
    utilisateurs = Utilisateur.objects.filter(is_superuser=False)
    serializer = UtilisateurSerializer(utilisateurs, many=True)
    return Response(serializer.data)

# Suppresion des token
@api_view(['POST'])
@permission_classes([AllowAny])
def delete_all_tokens(request):
    tokens = OutstandingToken.objects.all()
    tokens.delete()

    return Response({
        'message':'tokens supprimés'
    })