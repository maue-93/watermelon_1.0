from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .constants import VOTE_CHOICES, DEFAULT_REACTION, REACTION_CHOICES, VOTE_CHOICES, \
                        LOW_VOUCH, MEDIUM_VOUCH, HIGH_VOUCH, VOUCH_CHOICES

# end of imports

# Create your models here.
"""
    NOTICE: 1 - 
    TO DO : 1 - 
"""



"""
    last review : 12/29/2023 - by eliso morazara
    abstract model = ModelWithCreateUpdateContent

    USES:   1 - Any models that need created_at, updated_at, and content fields can inherit from it
            2 - Avoid errors in repetition

    INHERITING MODELS : 
        - Tags

    TO DO : 1 - Find out how to make the model be deleted when the content_objects is deleted.
"""
class ModelWithCreateUpdateContent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    class Meta:
        abstract = True
# end of ModelWithCreateUpdateContent
        

"""
    last review : 01/27/2024 - by eliso morazara
    abstract model = ModelWithCreateUpdateAuthorContent

    USES:   1 - Any models that need created_at, updated_at, author, and content fields can inherit from it
            2 - Avoid errors in repetition

    INHERITING MODELS : 
        - Post
        - Comments
        - Reactions
        - Votes

    TO DO : 1 - Find out how to make the model be deleted when the content_objects is deleted.
"""
class ModelWithCreateUpdateAuthorContent(ModelWithCreateUpdateContent):
    author_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_object_id = models.PositiveIntegerField()
    author_object = GenericForeignKey('author_content_type', 'author_object_id')
    class Meta:
        abstract = True
# end of ModelWithCreateUpdateAuthorContent


"""
    last review : 01/04/2024 - by eliso morazara

    MODEL = Post : a record of activities that other users can interact with

    USES :  1 - An easy and uniform way to record both session activities and regular posts 

    WHY :   1 - This is the easiest and most user friendly way we have found to post different kinds of sessions and 
                regular posts in fewer clicks

    HOW IT WORKS:
            1 - There are 3 types of posts : 
                1 - Session : A work session, with more precise time, with a list of tasks and comments
                2 - InstantSession : Quick session (up to DEFAULT_INSTANT_SESSION_MINUTES_LIMIT minutes), with only the 
                    time it is posted, with a list of tasks and comments
                3 - Non-Session : Just a regular post in which there is no session or list of tasks
            2 - There are 2 ways to create a post:
                1 - After deactivating an active status on a project (Session Post)
                2 - Click a button available in all pages to create a Post which is by default an Instant Session Post
            3 - After a Post creation :
                1 - Verify the type of Post; change if necessary
                2 - Add text and media content to the Post
                3 - If Session (not Instant Session) Post, verify the session time; change if necessary
                4 - Add list of tasks if a Session (or Instant Session) Post
                5 - Click the post button

    NOTICE: 1 - The author is a UserAccess (defined in project app)
            2 - The content is a regular post, Project, new UserAccess, AccessRequest, RemovalRequest, DeleteRequest,
                or Session

    TO DO : 1 - Find out if a sesion should have the ability to be on different posts
            2 - Add media content

    GENERIC RELATED FIELD : 
        - content_comments : model = Comment : a set of comments directly posted on this post; the reply comments are 
                                                linked to the parent comments
        - content_reactions : model = Reaction : set of reactions that this post has
"""
class Post (ModelWithCreateUpdateAuthorContent):
    author_content_type = models.ForeignKey(ContentType, related_name='posts', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='posted', on_delete=models.CASCADE)
    text_content = models.TextField()
# end of Post


"""
    last review : 01/04/2024 - by eliso morazara

    MODEL = Comment : a comment on a post

    USES :  1 - A tool for non-author to interact with the post besides reaction to it

    WHY :   1 - This is an important feature in a collaborative space because it allows interaction on a specific post at
                the right place

    HOW IT WORKS :
            1 - Commenting on a post or replying to a comment

    NOTICE: 1 - The author is a UserAccess (defined in project app) or the Core.User defined in settings.AUTH_USER_MODEL
            2 - The content field is a Post 

    TO DO : 1 - Should a comment have a media content?

    RELATED FIELDS : 
        - replies : model = Comment : set of all reply comments under this one
"""
class Comment (ModelWithCreateUpdateAuthorContent):
    author_content_type = models.ForeignKey(ContentType, related_name='commented', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='comments', on_delete=models.CASCADE) 
    comment = models.TextField()
    parent = models.ForeignKey('Comment', related_name='replies', null=True, on_delete=models.CASCADE)
# end of Comments
    

"""
    last review : 01/27/2024 - by eliso morazara

    MODEL = Reaction : a reaction to a post, comment, or more

    USES :  1 - A database of Users' reactions to Post, comment or more

    WHY :   1 - It is an easy fast forward way to understand others' feelings about a post or comment
            2 - It is an easy way to acknoledge that you read the comment

    HOW IT WORKS :
            1 - Click on the reaction button and choose one of the options.

    NOTICE: 1 - The content generic field is a Post or comment

    TO DO : 1 - What sorts of reactions should be made available?
            2 - Should we also add reactions to comments? It is kind of an easy way to acknoledge that you read the 
                comment. If we add reaction to coments, should we just add a "comment_reactions" to the comment in Comments?
"""
class Reaction (ModelWithCreateUpdateAuthorContent):
    author_content_type = models.ForeignKey(ContentType, related_name='reacted', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='reactions', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=1, default=DEFAULT_REACTION, choices=REACTION_CHOICES)
# end of Reaction


"""
    last review : 01/27/2024 - by eliso morazara

    MODEL = Vote : set of all votes or vouches

    USES :  1 - Keep track of the votes for AccessRequest, RemovalRequest, and DeleteRequest

    WHY :   1 - It is very important to add a sort of democratic features in adding or removing someone to or from the
                project

    HOW IT WORKS :
            1 - Clicking on a button to vote

    NOTICE: 1 - The content field is AccessRequest, RemovalRequest, and DeleteRequest
            2 - Still not sure if implementing this in the first version

    TO DO : 1 - Revise the voting options defined in constants.py
"""
class Vote (ModelWithCreateUpdateAuthorContent):
    author_content_type = models.ForeignKey(ContentType, related_name='voted', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='votes', on_delete=models.CASCADE)
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)
# end of Vote


"""
    last review : 01/27/2024 - by eliso morazara

    MODEL = Vouch : a vouch instance to vouch for a session or else

    USES :  1 - Track vouches that a Session gets (a measurement for credibility of the post)

    WHY :   1 - It is important that we allow others to vouch for the work we report (it will add credibility to the post)

    HOW IT WORKS :
            1 - Click a button on the post to vouch for it

    NOTICE: 1 - The content field is a Session
            2 - Not really sure if we should use this in the first version

    TO DO : 1 - Revise the vouching options defined in constants.py
"""
class Vouch (ModelWithCreateUpdateAuthorContent):
    author_content_type = models.ForeignKey(ContentType, related_name='vouched', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='vouches', on_delete=models.CASCADE)
    vouche = models.CharField(max_length=1, default=MEDIUM_VOUCH, choices=VOUCH_CHOICES)
# end of Vouch


"""
    last review : 01/27/2024 - by eliso morazara

    MODEL = Tags : set of tags that a content has

    USES :  1 - Tag a Topic or more to a Task

    WHY :   1 - It is important to tag Topic to a Task for easier data analytics on time spent on the project

    HOW IT WORKS :
            1 - At the creation of a Task, one can tag a Topic or more to it
            2 - The topic will be created if not existant and then tagged
            3 - The user should also be able to see how many times that tag was used in the app

    NOTICE: 1 - The content generic field is Task
            2 - The tag_object is a Topic defined in the project app

    TO DO : 1 - Set up the JSONField
"""
class Tag (ModelWithCreateUpdateContent): 
    content_type = models.ForeignKey(ContentType, related_name='tags', on_delete=models.CASCADE)
    tag_content_type = models.ForeignKey(ContentType, related_name='tagged', on_delete=models.CASCADE)
    tag_object_id = models.PositiveIntegerField()
    tag_object = GenericForeignKey('tag_content_type', 'tag_object_id')
# end of Tag
