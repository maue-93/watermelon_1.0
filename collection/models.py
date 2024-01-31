from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

"""
    IMPORTANT NOTICE : 
        1- A collection belongs to a user
        2- A user can add their own project to the collection or a project they are part of
"""


"""
    last review : 01/04/2024 - by eliso morazara
    
    MODEL = Collection : a collection of projects

    USES :  1 - To put together projects you are part of in different categories

    WHY :   1 - Useful to organize oneself

    HOW IT WORKS :
            1 - Create a collection and add project 
            2 - The content_type is UserAccess. This way we only retrieve the projects this user has active access to
            3 - The project ids are stored in a JSONField field collected_objects in the following format:
                [
                    {
                        "object_ids" = {___, ___, ___, ....}
                    }
                ]

    NOTICE: 1 - The author is the Core.User

    TO DO : 1 - Is 150 a good max_length for the title?
            2 - Add parent collection.
"""
class Collection (models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)

    author_content_type = models.ForeignKey(ContentType, related_name='collections', on_delete=models.CASCADE)
    author_object_id = models.PositiveIntegerField()
    author_object = GenericForeignKey('author_content_type', 'author_object_id')

    content_type = models.ForeignKey(ContentType, related_name='content_type_collections', on_delete=models.CASCADE)
    collected_objects = models.JSONField()
 # end of Collection   


# class Favorites 
