from rest_framework import serializers
from generic_relations.relations import GenericRelatedField

from project.models import Project, UserAccess, AccessRequest, RemovalRequest, Progress, Session, Task, Topic
from project.serializers import ProjectSerializer, UserAccessSerializer, AccessRequestSerializer, RemovalRequestSerializer,\
                                ProgressSerializer, SessionSerializer, TaskSerializer, TopicSerializer

from .models import Post, Comment, Reaction, Vote, Vouch, Tag


"""
    RESOURCES : https://pypi.org/project/rest-framework-generic-relations/

"""


"""
    last review : 01/12/2024 - by eliso morazara

    SERIALIZER = PostSerializer : Serializer for the Post model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
    
"""
class PostSerializer (serializers.ModelSerializer):
    author_object = GenericRelatedField(
        {
            UserAccess : UserAccessSerializer(),
            # probably should add the core user as well
        }
    )

    content_object = GenericRelatedField(
        {
            Project : ProjectSerializer(),
            UserAccess : UserAccessSerializer(),
            AccessRequest : AccessRequestSerializer(),
            RemovalRequest : RemovalRequestSerializer(),
            Progress : ProgressSerializer(),
            Session : SessionSerializer()
        }
    )

    class Meta:
        model = Post
        fields = ['author_object', 'content_object']
# end of PostSerializer
        

"""
    RESOURCES : https://pypi.org/project/rest-framework-generic-relations/

"""


"""
    last review : 01/12/2024 - by eliso morazara

    SERIALIZER = CommentSerializer : Serializer for the Comment model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
    
"""
class CommentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content_object', 'comment']
    # end of Meta
    content_object = GenericRelatedField(
        {
            Post : PostSerializer()
        }
    )
    # def create(self, validated_data):
    #     return super().create(validated_data)
    
# end of CommentSerializer


"""
    last review : 01/12/2024 - by eliso morazara

    SERIALIZER = ReactionSerializer : Serializer for the Reaction model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
    
"""
class ReactionSerializer (serializers.ModelSerializer):
    content_object = GenericRelatedField(
        {
            Post : PostSerializer()
        }
    )
    class Meta:
        model = Reaction
        fields = ['content_type', 'reaction']
# end of ReactionsSerializer
        

"""
    last review : 01/12/2024 - by eliso morazara

    SERIALIZER = VoteSerializer : Serializer for the Vote model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
    
"""
class VoteSerializer (serializers.ModelSerializer):
    content_object = GenericRelatedField(
        {
            AccessRequest : AccessRequestSerializer(),
            RemovalRequest : RemovalRequestSerializer()
        }
    )
    class Meta:
        model = Vote
        fields = ['content_type', 'vote']
    # end of Meta
    # def create(self, validated_data):
    #     return 
# end of VotesSerializer


"""
    last review : 01/12/2024 - by eliso morazara

    SERIALIZER = VouchSerializer : Serializer for the Vouch model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
    
"""
class VouchSerializer (serializers.ModelSerializer):
    content_object = GenericRelatedField(
        {
            Session : SessionSerializer()
        }
    )
    class Meta:
        model = Vouch
        fields = ['content_object', 'vouches']
# end of VouchesSerializer


"""
    last review : 01/12/2024 - by eliso morazara

    SERIALIZER = TagSerializer : Serializer for the Tag model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
    
"""
class TagSerializer (serializers.ModelSerializer):
    content_object = GenericRelatedField(
        {
            Task : TaskSerializer()
        }
    )

    tag_object = GenericRelatedField(
        {
            Topic : TopicSerializer()
        }
    )
    class Meta:
        model = Tag
        fields = ['content_object', 'tag_object']

