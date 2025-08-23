from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny

from django.contrib.auth.tokens import default_token_generator

from account.models import Utilisateur
from django.conf import settings

from .serializers import PasswordResetSerializers, PasswordChangeSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):

    # recuperer l'email de l'utilisateur
    serializer = PasswordResetSerializers(data=request.data)
    
    email = request.data.get('account_email')

    # Verifier que l'email n'est pas vide
    if email is None or serializer.is_valid() :
        return Response({
            "error":"Veuillez saisir l'email"
        }, status=status.HTTP_200_OK)

    # Verifier que l'email existe
    try :
        user = Utilisateur.objects.get(account_email = email)
    except Utilisateur.DoesNotExist:
        return Response({
            "error":"Cet email n'est lié à aucun compte"
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Creation de la clé pour renitialiser le mot de passe
    token = default_token_generator.make_token(user)
    uid = user.pk
    reset_url = f"{settings.FRONTEND_URL}/change_password/{uid}/{token}/"

    
    # envoi de mail pour recupérer ou changer le mot de passe
    send_mail(
        subject="Renitialisation de mot de passe",
        message=f"Renitialiser votre mot de passe {reset_url}",
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]  
    )
    return Response({
        'message':'Veuillez consulter votre email pour renitialiser le mot de passe'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request,uid,token):
    
    # Verifier l'existance du nouveau mot de passe
    serializer = PasswordChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    new_password = request.data.get('new_password')

    # Verifier que l'utilisateur existe
    try:
        user = Utilisateur.objects.get(pk=uid)
    except Utilisateur.DoesNotExist:
        return Response({
            'error':'Utilisateur inexistant'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifier que le token généré est toujours valide
    if not default_token_generator.check_token(user, token):
        return Response({
            'error':'Token Invalide ou Expiré'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Changer le mot de passe
    user.set_password(new_password)
    user.save()
    return Response({
        'message':'mot de passe modifié avec succès'
    }, status=status.HTTP_200_OK)