from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Tache, SousTache
from .serializer import TacheSerializer, SousTacheSerializer
from account.models import Utilisateur

from django.db.models import Q


# Create your views here.

# CRUD de Tache

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_tache(request):
    try :
        liste_tache = Tache.objects.filter(
            Q(proprietaire=request.user) | Q(collaborateurs=request.user)
            )
        if not liste_tache.exists():    
            return Response({
                'detail':'aucune tache trouvée'
            }, status=status.HTTP_204_NO_CONTENT)
    except Tache.DoesNotExist:
        return Response({
            "detail":"Erreur interne"
        }, status=status.HTTP_204_NO_CONTENT)
    
    serializer = TacheSerializer(liste_tache, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tache(request):
    account_email = request.data.get('account_email')
    nom_tache = request.data.get('nom_tache')
    status_tache = request.data.get('status_tache')
    
    if Tache.objects.filter(proprietaire=account_email, nom_tache = nom_tache ,status_tache=status_tache).exists():
        return Response({
            "error":"Cette tache existe dejà"
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = TacheSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(proprietaire=request.user)
        return Response({
            'message':'nouvelle tache ajoutée',
            'detail' : serializer.data
        }, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def detail_tache(request, pk):
    try :
        detail_tache = Tache.objects.get(id=pk)

    except Tache.DoesNotExist:
        return Response({
            'detail':'Aucune tache trouvée'
        }, status=status.HTTP_204_NO_CONTENT)
    
    # Verifier la permission
    if request.user != detail_tache.proprietaire and request.user not in detail_tache.collaborateurs.all():
        return Response({
            'detail':'vous êtes pas autorisé'
        }, status=status.HTTP_403_FORBIDDEN)
    

    if request.method == 'GET':
        serializer = TacheSerializer(detail_tache)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    if request.method == 'DELETE':
        detail_tache.delete()
        return Response({
            'message':'Element supprimé'
        }, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = TacheSerializer(detail_tache, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(proprietaire=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# CRUD de Sous Tache

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sous_tache(request, tache_id):

    try:
        tache = Tache.objects.get(id=tache_id)
    except Tache.DoesNotExist:
        return Response({
            'detail':'La tache est inexistante'
        })
    
    # Verifier la permission
    if request.user != tache.proprietaire and request.user not in tache.collaborateurs.all():
        return Response({
            'detail':'vous êtes pas autorisé'
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = SousTacheSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(tache=tache)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def detail_sous_tache(request, sous_tache_id):
    try:
        sous_tache = SousTache.objects.get(id=sous_tache_id)
    except SousTache.DoesNotExist:
        return Response({
            "detail":'aucun element trouvé'
        }, status=status.HTTP_200_OK)
    
    # Verifier la permission
    tache_ = sous_tache.tache
    if request.user != tache_.proprietaire and request.user not in tache_.collaborateurs.all():
        return Response({
            'detail':'Accès non autorisé'
        })
    

    if request.method == 'GET':
        serializer = SousTacheSerializer(sous_tache)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    if request.method == 'DELETE':
        sous_tache.delete()
        return Response({
            'detail':'tache supprimée'
        }, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = SousTacheSerializer(sous_tache, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                


# Ajout des collaborateurs
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajout_collaborateurs(request,tache_id):
    try:
        tache = Tache.objects.get(id=tache_id, proprietaire=request.user)
    except Tache.DoesNotExist:
        return Response({
            'detail':'tache inexistante'},status=status.HTTP_404_NOT_FOUND)
    
    collaborateur = request.data.get('emailCollaborateur')

    if collaborateur is None :
        return Response({
            'detail':'veuillez ajouter un collaborateur'
        })


    try:
        user_add = Utilisateur.objects.get(account_email=collaborateur)
    except Utilisateur.DoesNotExist:
        return Response({
            'detail':'Compte non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)

    # Verifier que l'utilisateur connecté n'est pas le collaborateur
    if request.user == user_add:
        return Response({
            'detail':'vous ne pouvez pas vous ajouter vous-même'
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    # Verifier que le collaborateur n'existe pas
    if tache.collaborateurs.filter(account_email=user_add).exists():
        return Response({
            'detail':'Vous collaborez deja avec cet utilisateur'
        }, status=status.HTTP_409_CONFLICT)
    

    tache.collaborateurs.add(user_add)
    return Response({
        'detail':'Collaborateur ajouté'
    }, status=status.HTTP_201_CREATED)

# Suppression d'un collaborateur
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def suppression_collaborateurs(request, pk,email_collaborateur):
    try :
        detail_tache = Tache.objects.get(id=pk)
    except Tache.DoesNotExist:
        return Response({
            'detail':'Aucune tache trouvée'
        }, status=status.HTTP_204_NO_CONTENT)
    
    try :
        user_deleted = Utilisateur.objects.get(account_email=email_collaborateur)
    except Utilisateur.DoesNotExist:
        return Response({
            'detail':'Collaborateur inexistant'
        }, status=status.HTTP_204_NO_CONTENT)

    
    if request.method == 'DELETE':
        detail_tache.collaborateurs.remove(user_deleted)
        return Response({
            'detail':'collaborateur supprimée'
        }, status=status.HTTP_200_OK)