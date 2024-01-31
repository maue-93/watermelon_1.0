from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action

from .models import Post, Comment, Reaction, Vote, Vouch, Tag
from .serializers import PostSerializer, CommentSerializer, ReactionSerializer, VoteSerializer, VouchSerializer,\
                        TagSerializer

# Create your views here.
"""
    last review : 01/12/2024 - by eliso morazara
    
    VIEWSET = PostViewSet : View set for Post model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class PostViewSet (ModelViewSet):
    def get_queryset(self):
        return Post.objects.all()
    def get_serializer_class(self):
        return PostSerializer
# end of PostViewSet


"""
    last review : 01/12/2024 - by eliso morazara
    
    VIEWSET = CommentViewSet : View set for Comment model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class CommentViewSet (ModelViewSet):
    def get_queryset(self):
        return Comment.objects.all()
    def get_serializer_class(self):
        return CommentSerializer
# end of CommentViewSet


"""
    last review : 01/12/2024 - by eliso morazara
    
    VIEWSET = ReactionViewSet : View set for Reaction model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class ReactionViewSet (ModelViewSet):
    def get_queryset(self):
        return Reaction.objects.all()
    def get_serializer_class(self):
        return ReactionSerializer
# end of ReactionViewSet


"""
    last review : 01/12/2024 - by eliso morazara
    
    VIEWSET = VoteViewSet : View set for Vote model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class VoteViewSet (ModelViewSet):
    def get_queryset(self):
        return Vote.objects.all()
    def get_serializer_class(self):
        return VoteSerializer
# end of VoteViewSet


"""
    last review : 01/12/2024 - by eliso morazara
    
    VIEWSET = VouchViewSet : View set for Vouch model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class VouchViewSet (ModelViewSet):
    def get_queryset(self):
        return Vouch.objects.all()
    def get_serializer_class(self):
        return VouchSerializer
# end of VouchViewSet


"""
    last review : 01/12/2024 - by eliso morazara
    
    VIEWSET = TagViewSet : View set for Tag model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class TagViewSet (ModelViewSet):
    def get_queryset(self):
        return Tag.objects.all()
    def get_serializer_class(self):
        return TagSerializer
# end of TagViewSet




