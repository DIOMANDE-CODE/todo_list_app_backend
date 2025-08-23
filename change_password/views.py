from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny

from account.models import Utilisateur
from django.conf import settings

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):

    # recuperer l'email de l'utilisateur
    email = request.data.get('account_email')
    print('reinitialisation ',email)

    # Verifier que l'email n'est pas vide
    if email is None :
        return Response({
            "error":"Veuillez saisir l'email"
        }, status=status.HTTP_200_OK)

    # Verifier que l'email existe
    try :
        Utilisateur.objects.get(account_email = email)
    except Utilisateur.DoesNotExist:
        return Response({
            "error":"Cet email n'est lié à aucun compte"
        }, status=status.HTTP_404_NOT_FOUND)

    
    # envoi de mail pour recupérer ou changer le mot de passe
    send_mail(
        subject="Renitialisation de mot de passe",
        message="Renitialiser votre mot de passe",
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]  
    )
    return Response({
        'message':'Veuillez consulter votre email pour renitialiser le mot de passe'
    }, status=status.HTTP_200_OK)