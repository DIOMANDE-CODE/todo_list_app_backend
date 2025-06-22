from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import TaskGroup, Task
from .serializer import TaskGroupSerializer, TaskSerializer
from account.models import Utilisateur

from django.db.models import Q


# Create your views here.

# CRUD de TaskGroup
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_groupe_tache(request):
    try :
        liste_groupe = TaskGroup.objects.filter(
            Q(proprietaire=request.user) | Q(collaborateurs=request.user)
            )
        if not liste_groupe.exists():
            return Response({
                'detail':'aucun element trouvé'
            }, status=status.HTTP_204_NO_CONTENT)
    except TaskGroup.DoesNotExist:
        return Response({
            "detail":"Erreur interne"
        }, status=status.HTTP_204_NO_CONTENT)
    
    serializer = TaskGroupSerializer(liste_groupe, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_groupe_tache(request):
    serializer = TaskGroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(proprietaire=request.user)
        return Response({
            'detail':'nouveau group ajouté',
            'groupe tache' : serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def detail_groupe_tache(request, pk):
    try :
        detail_groupe = TaskGroup.objects.get(id=pk)

    except TaskGroup.DoesNotExist:
        return Response({
            'detail':'Aucun element trouvé'
        }, status=status.HTTP_204_NO_CONTENT)
    
    # Verifier la permission
    if request.user != detail_groupe.proprietaire and request.user not in detail_groupe.collaborateurs.all():
        return Response({
            'detail':'vous êtes pas autorisé'
        }, status=status.HTTP_403_FORBIDDEN)
    

    if request.method == 'GET':
        serializer = TaskGroupSerializer(detail_groupe)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    if request.method == 'DELETE':
        detail_groupe.delete()
        return Response({
            'detail':'Element supprimé'
        }, status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'PUT':
        serializer = TaskGroupSerializer(detail_groupe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(proprietaire=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





# CRUD de Task

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tache(request, groupe_tache_id):

    try:
        groupe_tache = TaskGroup.objects.get(id=groupe_tache_id)
    except TaskGroup.DoesNotExist:
        return Response({
            'detail':'groupe tache inexistant'
        })
    
    # Verifier la permission
    if request.user != groupe_tache.proprietaire and request.user not in groupe_tache.collaborateurs.all():
        return Response({
            'detail':'vous êtes pas autorisé'
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(groupe_tache=groupe_tache)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def detail_tache(request, tache_id):
    try:
        tache = Task.objects.get(id=tache_id)
    except Task.DoesNotExist:
        return Response({
            "detail":'aucun element trouvé'
        }, status=status.HTTP_200_OK)
    
    # Verifier la permission
    groupe_tache_ = tache.groupe_tache
    if request.user != groupe_tache_.proprietaire and request.user not in groupe_tache_.collaborateurs.all():
        return Response({
            'detail':'Accès non autorisé'
        })
    

    if request.method == 'GET':
        serializer = TaskSerializer(tache)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    if request.method == 'DELETE':
        tache.delete()
        return Response({
            'detail':'tache supprimée'
        }, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = TaskSerializer(tache, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                


# Ajout des collaborateurs
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajout_collaborateurs(request,groupe_id):
    try:
        tache_groupe = TaskGroup.objects.get(id=groupe_id, proprietaire=request.user)
    except TaskGroup.DoesNotExist:
        return Response({
            'detail':'groupe tache inexistant'},status=status.HTTP_404_NOT_FOUND)
    
    collaborateur = request.data.get('email')


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
        }, status=status.HTTP_200_OK)
    
    tache_groupe.collaborateurs.add(user_add)
    return Response({
        'detail':'Collaborateur ajouté'
    }, status=status.HTTP_201_CREATED)