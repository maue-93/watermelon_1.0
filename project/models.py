from uuid import uuid4
import json

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from post.models import Tag

# import custom metrics for more flexibility
from .constants import  DEFAULT_DIFFICULTY, DIFFICULTY_CHOICES, \
                        DEFAULT_WEIGHT, WEIGHT_CHOICES, DEFAULT_RATE_COMPLETE_STATUS,\
                        DEFAULT_TOPIC_TITLE_MAX_LENGTH

# end of imports


"""
    last review : 02/05/2024 - by eliso morazara
    NOTICE: 1 - Use of settings.AUTH_USER_MODEL >> that is set to core.User >> in project settings >> defined in core

    TO DO : 1 - Correctly set up the fields that have values depending on other fields
            2 - Correctly set up the default values  
            3 - Set up __str__ for each model
"""


# Create your models here.
"""
    last review : 02/07/2024 - by eliso morazara

    ABSTRACT MODEL = WithCreateUpdateTrashTime

    USES:   1 - Any models that need created_at, updated_at, and trashed_at fields can inherit from it
            2 - Avoid errors in repetition

    INHERITING MODELS : 
        - Project
        - AccessRequest
        - UserAccess
        - RemovalRequest
        - Progress
        - Session
        - Task
"""
class WithCreateUpdateTrashTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trashed_at = models.DateTimeField(null=True)
    class Meta:
        abstract = True
# end of WithCreateUpdateTrashTime

class MyModel(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

# end of MyModel

"""
    last review : 02/07/2024 - by eliso morazara

    MODEL = Project : a project/goal

    USES :  1 - A base point to track progress of a project and its parent project

    WHY :   1 - Understanding how far you have come and how far there is left to go in your project is essential

    HOW IT WORKS : 
            1 - To create a project, add the title, optional description, optional deadline, and optional image
            2 - After you have created the project, if not root project, it asks you to input difficulty and weight to the 
                project
            3 - Then after that, it asks if you want to invite someone to the project.

    NOTICE: 1 - If change Model Class Name, MAKE SURE to update model string name in parent field
            2 - The creator of the project is determined by the UserAccess model;
                a - The related field name in Project is "user_accesses", 
                b - Then look for a UserAccess that has the field is_creator as True
            3 - The is_complete field is True when more than DEFAULT_RATE_COMPLETE_STATUS% users have marked it complete
            4 - To find the difficulty and weight of a project, we use the related user_accesses field
            5 - To find how much difficulty or weight has been tackled, we use the related progresses field
    TO DO : 1 - Add a deadline default value of 2 weeks from creation
            2 - Set up permissions, as of now the idea is to have an editor, commentor, and viewer permissions.
                a - This will also affect AccessRequest and UserAccess
            3 - Review difficulty and weight defaults and choices
            4 - Make sure we have a code to make is_complete True when number of complete marks is met
            5 - Find out if editable=True in deadline field is necessary
            6 - Add a discusion Q&A platform (project). At the to of group assignment for example. 
                Simple posts in the project can be used to do this. 
            7 - Add an image field

    RELATED FIELDS :
        - subprojects : model = Project : sub-projects of this project
        - user_accesses : model = UserAccess : set of links between this project and users
        - progresses : model = Progress : set of progresses made on this project
        - topics : model = Topics : set of task topics in this project, their hierarchy can be retrieved from them
"""
class Project (WithCreateUpdateTrashTime):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True) 
    deadline = models.DateField(editable=True, null=True, blank=True) 
    is_complete = models.BooleanField(default=False)
    parent = models.ForeignKey("Project", related_name='subprojects', null=True, on_delete=models.CASCADE)
# end of Project


"""
    last review : 02/07/2024 - by eliso morazara

    MODEL = UserAccess : a user access to a project

    USES :  1 - A long term token for a user to have access to a project
            2 - Can see who is active on the project at the moment
            3 - A user can assign difficulty and weight to the project (if not root project)

    HOW IT WORKS : 
            1 - A UserAccess is created at the creation of a project (the is_creator is True)
            2 - Each time a user has accepted an invite, a UserAccess is created
            3 - Each time a user whose request to join is accepted, a UserAccess is created
            4 - The has_access field is False when the user is removed from the project
            5 - If a user had access before, then removed, then invited back:
                a - no extra UserAccess is created
                b - only the has_access field is changed back to True
            6 - The is_active field is True when the user is currently working on this project
            7 - The mark_complete field is True when the user marks the project complete
            8 - The show_project field is False when the user decide to hide the projects from feed, notifications, and
                most of the features in the app
            9 - It is never deleted unless the project is deleted

    NOTICE: 1 - We should worry about is_creator only at the creation of the project
            2 - A project can have many creators
            3 - The has_access field is False when the user is removed from the project
            
    TO DO : 1 - Could it be useful for a project to be able to have many creators?
            2 - If Yes, Think of ways for a project to have many creators at creation

    RELATED FIELDS :
        - invites : model = AccessRequest : set of invites sent from the user of this access to join this project
        - removals_out : model = RemovalRequest : set of requests from the user to remove another user' access to the project
        - removals_in : model = RemovalRequest : set of requests from other users to remove this access
        - access_requests : model = AccessRequest : set of access requests that have created or changed this user access
        - removal_requests : model = RemovalRequest : set of requests to invalidate this UserAccess
        - sessions : model = Session : set of sessions done by this user on this project
"""
class UserAccess (WithCreateUpdateTrashTime):
    project = models.ForeignKey(Project, related_name='user_accesses', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_accesses', null=True, on_delete=models.SET_NULL)
    is_creator = models.BooleanField(default=False)
    has_access = models.BooleanField(default=True)
    show_project = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    mark_complete = models.BooleanField(default=False)
    difficulty = models.PositiveSmallIntegerField(default=DEFAULT_DIFFICULTY, choices=DIFFICULTY_CHOICES)
    weight = models.PositiveSmallIntegerField(default=DEFAULT_WEIGHT, choices=WEIGHT_CHOICES)
# end of UserAccess


"""
    last review : 02/07/2024 - by eliso morazara
    MODEL = AccessRequest : invitation or request to join a project

    USES :  1 - For a user that has access : Sends an invite to a user to join their project or sub-project
            2 - For a user without access : Sends a request to join a project or sub-project

    HOW IT WORKS :
            1 - In case of invite: Enter the name or username of the user(s) to invite
            2 - In case of request: Click on the project of concern, click on join button
            1 - The is_invite field is True when a user with access invite a user to join the project
            2 - The is_accepted field is True when the invitee accepts the invite or when someone in the project accepts 
                the request.
            2 - The is_declined field is True when the invitee decline the invite or when someone in the project declines 
                the request.
            4 - A UserAccess is created if accepted and if the user has never been an associate on this project. Then
                user_access = the created access
            5 - If the user already has an invalid access, the has_access field of the access is turned back to True and
                user_access = that access
                
    NOTICE: 1 - 

    TO DO : 1 - Add a is_past_due field that will be True when this access request is 
                DEFAULT_DAYS_TO_ACCESS_REQUEST_DEADLINE old or more.

    RELATED FIELDS : 
        - 
"""
class AccessRequest (WithCreateUpdateTrashTime):
    is_invite = models.BooleanField()
    is_accepted = models.BooleanField(default=False) # true if the invitee or a collaborator accepts
    is_declined = models.BooleanField(default=False) # true if the invitee or a collaborator decline
    inviter_access = models.ForeignKey(UserAccess, related_name='invites', null=True, on_delete=models.SET_NULL)
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='access_requests', null=False, 
                                on_delete=models.CASCADE)
    user_access = models.ForeignKey(UserAccess, related_name='access_requests', null=True, on_delete=models.SET_NULL)
# end of AccessRequest


"""
    last review : 12/30/2023 - by eliso morazara
    MODEL = RemovalRequest : a request to invalidate someone's access from a project

    USES :  1 - Request to remove someone's access from the project
            2 - Removing oneself from the project

    HOW IT WORKS: 
            1 - Once REMOVE_ASSOCIATE_VOTE_RATE % of the group approve, is_approved becomes True, 
                then the has_access field in the access_to_invalidate to False
            2 - In case a user removes themself: 
                a - the requester_access and access_to_invalidate are the same
                b - is_approved is right away True
                c - the has_access field in the access_to_invalidate becomes False


    NOTICE: 1 - 

    TO DO : 1 - Add a is_past_due field that will be True when this RemovalRequest is 
                DEFAULT_DAYS_TO_REMOVAL_REQUEST_DEADLINE old or more.
"""
class RemovalRequest (WithCreateUpdateTrashTime): 
    is_approved = models.BooleanField()
    requester_access = models.ForeignKey(UserAccess, related_name='removals_out', null=True, on_delete=models.SET_NULL)
    access_to_invalidate = models.ForeignKey(UserAccess, related_name='removals_in', on_delete=models.CASCADE)
# end of RemovalRequest


"""
    last review : 12/31/2023 - by eliso morazara

    MODEL = Progress : tracks progress of a project

    USES :  1 - Understanding how a project is going.

    WHY :   1 - Real time feedback on how the project is progressing.
            2 - Peace of mind knowing and peace of mind not having to make unnecessary meetings or unnecessary check ins.
            3 - Now you can make meetings or check ins for only when it matters, and you can use the app to find out
                what parts are not moving and who to check in with.
    
    HOW IT WORKS : 
            1 - One Progress object of 0% difficulty and 0% weight tackled is created at creation of project
            2 - The difficulty and weight field is the amount takled for the Project at creation of Progress
            3 - Progress has a data_points JSONField that can contain DEFAULT_DATA_POINT_NUMBER_IN_PROGRESS data points
            4 - Each data point has {"datetime" : ___ , "difficulty" : ___ , "weight" : ___}
            5 - Each data point is DEFAULT_MINUTES_BETWEEN_DATA_POINT_IN_PROGRESS after the previous one.
            6 - Every data point must have at least DEFAULT_POINT_DIFFERENCE_BETWEEN_DATA_POINT_IN_PROGRESS difference in
                either difficulty or weight tackled compared to the previous data point
            7 - When a Progress has DEFAULT_DATA_POINT_NUMBER_IN_PROGRESS data_points, next time after 
                DEFAULT_MINUTES_BETWEEN_DATA_POINT_IN_PROGRESS, a new Progress object is created.
            8 - However, if is_complete in Project is True because the group has agreed that the project is finished,
                a data point of 100% difficulty and 100% weight tackled is automatically created. If they agree to 
                reopen the project, an appropriate data point will be automatically created.
    
    NOTICE: 1 - The difficulty and weight fields data are also stored in data_points with :
                {"datetime" : created_at , "difficulty" : ___ , "weight" : ___}
            2 - We have the difficulty and weight data as fields at creation of the Progress as a back up if anything 
                happens to data_points. 
            3 - It might actually better to update only when there are change 
                a - in a project difficulty or weight
                b - in a project's complete status
                c - in the two cases above, then we update the json field for this project then all the parent and grandparent
                    and so on until the root project

    TO DO : 1 - Find out how to add fields and validators to the JSONField data_points
"""
class Progress (WithCreateUpdateTrashTime):
    project = models.ForeignKey(Project, related_name='progresses', on_delete=models.CASCADE, null=False)
    difficulty = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    data_points = models.JSONField()
# end of Progress


"""
    last review : 12/31/2023 - by eliso morazara

    MODEL = Session : A work session a user did on a project
    
    USES :  1 - Tracks working time of project associates
    
    WHY :   1 - Associates can see other's sessions and what they did
            2 - Self assessment
            3 - Data analytics on aggregate and individual times spent on the project

    HOW IT WORKS :
            1 - A session can be > or <= DEFAULT_INSTANT_SESSION_MINUTES_LIMIT.
            2 - A session that is <= DEFAULT_INSTANT_SESSION_MINUTES_LIMIT is called "Instant Session" and the is_instant
                field is True
            3 - An instant session do not need end_at, only the start_at
            4 - start_at is automatically the time the user marks active or the time the session post is created.
                However, it can be modified if desired
            3 - An associate can create a session by either :
                a - Manually creating a Session Post
                b - Marking themself active (is_active in Access) on a project. A Session and a Session Post are automatically 
                    created then finalized by the user at the end of session, when they mark themself inactive
            4 - A session is always part of a Post. The Post model is defined in the post app
    
    NOTICE: 1 - A Session object is always part of a Post that is tied to a UserAccess

    TO DO : 1 - Add validator to make sure end_at > start_at
            2 - Some session are garbage session so we need to make sure we delete them,
                example: a user is removed from the project while they are working on it
            3 - Should we have a default value for is_instant?

    RELATED FIELDS : 
        - tasks : model = Task : a set of tasks the user reports to have done durring this session
    
"""
class Session (WithCreateUpdateTrashTime):
    is_instant = models.BooleanField(default=True)
    user_access = models.ForeignKey(UserAccess, related_name='sessions', null=True, on_delete=models.SET_NULL)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
# end of Session


"""
    last review : 01/27/2024 - by eliso morazara
    
    MODEL = topic : topic of a task (example: anything email, database, django)
    
    USES :  1 - Classification of tasks
            2 - Data analystics by categories of tasks

    WHY :   1 - It could be useful to know what categories of tasks each associate spend their time on.

    HOW IT WORKS :
            1 - When a user reports a task they did, they can tag a topic or more to it
            2 - If the topic they want to tag has not been created by anyone using the app, they can create it

    NOTICE: 1 - 

    TO DO : 1 - Add code to make sure that the unique rules is case insensitive
            2 - maybe this should be not here but in a different app

    RELATED FIELDS : 
        - projects : model = TopicInProject : set of links between this topic and the projects it is used in
    
"""
class Topic (WithCreateUpdateTrashTime):
    title = models.CharField(max_length=DEFAULT_TOPIC_TITLE_MAX_LENGTH, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topics', null=True, on_delete=models.SET_NULL)
# end of Topic


"""
    last review : 01/27/2024 - by eliso morazara

    MODEL = TopicInProject : an instance of a topic used in a specific project

    USES :  1 - Build a hierarchy of topics in a certain project by using this model

    WHY :   1 - To maximize accuracy of data analytics

    HOW IT WORKS :
            1 - When an associate tags a topic to a task, if it has not been tagged in previous tasks in the app, we create
                an object of TopicInProject accordingly without a parent TopicInProject object
            2 - Then they can give hierarchy to the topics: what topic is a subtopic of what topic. That's the use of this

    NOTICE: 1 - Do not for get to update the parent field in case change the name of the class

    TO DO : 1 - Add a feature to make two task topics as equal even though they have different titles. 
                Figure out if this is a good idea first.
    
    RELATED FIELDS : 
        - subtopics : model : TopicInProject : set of subtopics of this topic in this project
"""
class TopicInProject(WithCreateUpdateTrashTime):
    topic = models.ForeignKey(Topic, related_name='projects', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='topics', on_delete=models.CASCADE)
    parent = models.ForeignKey("TopicInProject", related_name='subtopics', null=True, on_delete=models.CASCADE)
# end of TopicInProject


"""
    last review : 01/02/2024 - by eliso morazara
    
    MODEL = Task : task reported done

    USES :  1 - Keeping track of associate activities on a project

    WHY :   1 - To build a record of associate activities on a project 

    HOW IT WORKS :
            1 - An associate can create tasks on every Session (or insta Session) Post
            2 - The associate needs to give a short description
            3 - The default duration_estimate value is the remaining duration of the session devided by the number of tasks.
            4 - You can correct the duration_estimate of a task and the default would be reajusted for other tasks whose
                duration has not been corrected
            5 - The total duration_estimate of all tasks cannot exceed the duration of the Session

    NOTICE: 1 - As of now, every task belong to a Session or instant Session
            2 - A task is always part of a Session object that is always part of a Post that is tied to a UserAccess

    TO DO : 1 - Add default values to duration_estimate based on the what is described above

    RELATED FIELDS:
        - 
"""
class Task (WithCreateUpdateTrashTime):
    description = models.CharField(max_length=255)
    session = models.ForeignKey(Session, related_name='tasks', on_delete=models.CASCADE)
    duration_estimate = models.DurationField(null=True)
# end of Task

