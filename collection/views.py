from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action

from .models import Collection
from .serializers import CollectionSerializer

# Create your views here.


"""
    last review : 01/12/2024 - by eliso morazara
    
    VIEWSET = CollectionViewSet : ViewSet for Collection

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class CollectionViewSet (ModelViewSet):
    def get_queryset(self):
        return Collection.objects.all()
    def get_serializer_class(self):
        return CollectionSerializer
# end of CollectionViewSet
