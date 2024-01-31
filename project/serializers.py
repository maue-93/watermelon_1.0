from datetime import datetime
import json

from rest_framework import serializers
from .models import Project, UserAccess, AccessRequest, RemovalRequest, Progress, Session, Topic, TopicInProject, Task



"""
    last review : 01/09/2024 - by eliso morazara

    RESOURCES:
        - https://www.django-rest-framework.org/api-guide/fields/
        - https://www.django-rest-framework.org/api-guide/serializers/#modelserializer

    NOTICE: 1 - 

    TO DO : 1 - Create a serializer for each model
    
"""


"""
    last review : 01/09/2024 - by eliso morazara

    SERIALIZER = ProjectSerializer : Serializer for UserAccess model

    USES :  1 - Used to serialize (get) and deserialize (post, put, patch) the Project model in view set(s)

    WHY :   1 - Have to have this for the view set

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - Use filter to show only the projects that the user is part of

    TO DO : 1 - Find a way to have some fields as write only
            2 - Use filter to show only the projects that the user is part of
            3 - find a way to create a subproject under a project's endpoint (projects/projects/1 for example)
                The idea is to create a project, of which parent is automatically set to the current project
            4 - Should use json.JSONEncoder or not?
            5 - Find the best encoder
"""
class ProjectSerializer (serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'deadline', 'is_complete', 'parent', 
                  'subprojects',
                ]
        read_only_fields = ['is_complete', 'subprojects']
    def create(self, validated_data):
        project_created = super().create(validated_data)
        Progress.objects.create(project=project_created, difficulty=0, weight=0, 
                                data_points= json.dumps([{"datetime" : datetime.now().isoformat(), "difficulty" : 0 , "weight" : 0},])
                                )
        # need to check if there is a user logged in here
        # in other words, if the context has an active user
        # MIGHT ACTUALLY NOT NEED TO CHECK BECAUSE YOU HAVE TO BE SIGNED IN TO GET TO PROJECTS ANYWAY
        UserAccess.objects.create(is_valid=True, user=self.context['user'], is_creator=True, project=project_created)
        return project_created
# end of ProjectSerializer
    

"""
    last review : 01/09/2024 - by eliso morazara
    
    SERIALIZER = UserAccessSerializer : Serializer for UserAccess model

    USES :  1 - Used to serialize (get) and deserialize (post, put, patch) the UserAccess model in view set(s)

    WHY :   1 - Have to have this for the view set

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - Use filter to show only the projects that the user is part of

    TO DO : 1 - Override create method to create a project when creating a project
            2 - Use filter to show only the projects that the user is part of
"""
class UserAccessSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserAccess
        fields = ['is_valid', 'user', 'is_creator', 'is_active', 'project', 'mark_complete', 'difficulty', 'weight']
    # project_title = serializers.SerializerMethodField(method_name='get_project_title')
    # def get_project_title (self, user_access : UserAccess):
    #     return user_access.project.title
# end of UserAccessSerializer


"""
    last review : 01/10/2024 - by eliso morazara
    
    SERIALIZER = AccessRequestSerializer : Serializer for AccessRequest model

    USES :  1 - Used to serialize (get) and deserialize (post, put, patch) the AccessRequest model in view set(s)

    WHY :   1 - Have to have this for the view set

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - Use filter to show only the AccessRequest that the user is part of

    TO DO : 1 - Override create method to automatically link the appropriate inviter_access when creating a AccessRequest
            2 - Use filter to show only the AccessRequest that the user is part of
"""
class AccessRequestSerializer (serializers.ModelSerializer):
    class Meta:
        model = AccessRequest
        fields = ['is_invite', 'is_accepted', 'is_approved', 'inviter_access', 'invitee', 'user_access']
        read_only_fields = ['user_access']
# end of AccessRequestSerializer
        

"""
    last review : 01/10/2024 - by eliso morazara
    
    SERIALIZER = RemovalRequestSerializer : Serializer for RemovalRequest model

    USES :  1 - Used to serialize (get) and deserialize (post, put, patch) the RemovalRequest model in view set(s)

    WHY :   1 - Have to have this for the view set

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - Use filter to show only the RemovalRequest that the user is part of

    TO DO : 1 - Override create method to automatically link the appropriate requester_access when creating a RemovalRequest
            2 - Use filter to show only the RemovalRequest that the user is part of
"""
class RemovalRequestSerializer (serializers.ModelSerializer):
    class Meta:
        model = RemovalRequest
        fields = ['is_approved', 'requester_access', 'access_to_invalidate']
# end of RemovalRequestSerializer


"""
    last review : 01/10/2024 - by eliso morazara
    
    SERIALIZER = ProgressSerializer : Serializer for Progress model

    USES :  1 - Used to serialize (get) and deserialize (post, put, patch) the Progress model in view set(s)

    WHY :   1 - Have to have this for the view set

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class ProgressSerializer (serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['pk', 'project', 'difficulty', 'weight', 'data_points']
# end of ProgressSerializer


"""
    last review : 01/10/2024 - by eliso morazara
    
    SERIALIZER = SessionSerializer : Serializer for Session model

    USES :  1 - Used to serialize (get) and deserialize (post, put, patch) the Session model in view set(s)

    WHY :   1 - Have to have this for the view set

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['is_instant', 'user_access', 'start_at', 'end_at']
# end of SessionSerializer


"""
    last review : 01/10/2024 - by eliso morazara
    
    SERIALIZER = TopicSerializer : Serializer for Topic model

    USES :  1 - Used to serialize (get) and deserialize (post, put, patch) the Topic model in view set(s)

    WHY :   1 - Have to have this for the view set

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class TopicSerializer (serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title', 'author']
# end of TopicSerializer


"""
    last review : 01/11/2024 - by eliso morazara
    
    SERIALIZER = TopicHierarchySerializer : Serializer for TopicHierarchy model

    USES :  1 - Used to serialize (get) and deserialize (post, put, patch) the TopicHierarchy model in view set(s)

    WHY :   1 - Have to have this for the view set

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 
"""
class TopicInProjectSerializer (serializers.ModelSerializer):
    class Meta:
        model = TopicInProject
        fields = ['topic', 'project', 'subtopics']
# end of TopicHierarchySerializer


"""
    last review : 01/12/2024 - by eliso morazara
    
    SERIALIZER =  TaskSerializer : Serializer for the Task model

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - Figure out how to add the tags here and change the list
            2 - make sure to create the topic necessary and a TopicInProject object
"""

class TaskSerializer (serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['description', 'session', 'duration_estimate']
# end of TaskSerializer


