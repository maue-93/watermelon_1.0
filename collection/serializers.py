from rest_framework import serializers
from generic_relations.relations import GenericRelatedField

from core.models import User
from core.serializers import UserSerializer

from .models import Collection


"""
    last review : 01/12/2024 - by eliso morazara

    SERIALIZER = CollectionSerializer : Serializer for the Collection model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
    
"""
class CollectionSerializer (serializers.ModelSerializer):
    author_object = GenericRelatedField(
        {
            User : UserSerializer()
        }
    )
    class Meta:
        model = Collection
        fields = ['title', 'description', 'author_object', 'content_type', 'collected_objects']
# end of CollectionSerializer




