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

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

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
    
    if user.is_active == False:
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
    

# Fonctionnalité d'envoi d'email + activation de compte
def confirmation_par_email(email):
    
    # Recupérer l'utilisateur qui a ce mail
    user = Utilisateur.objects.get(account_email=email)

    # Générer un token de vérification
    token = default_token_generator.make_token(user)
    uid = user.pk
    activating_account_url = f"{settings.FRONTEND_URL}/activation/{uid}/{token}"

    # Envoi du mail de validation
    send_mail(
        subject="Activation de compte",
        message=f"Activer votre compte en cliquant sur ce lien {activating_account_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def activer_compte(request, uid, token):

    # recupérer l'utilisateur
    user = Utilisateur.objects.get(pk=uid)

    # Verifier que le token est valide
    if not default_token_generator.check_token(user,token):
        return Response({
            "error":"token invalide"
        }, status=400)
    
    # activer le compte
    user.is_active = True
    user.save()
    return Response({
        "message":"compte activé avec succès"
    }, status=200)


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
        confirmation_par_email(email)
        return Response({
                'message':'Veuillez consulter votre boite email pour activer votre compte',
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

# -----------------------------------------------------