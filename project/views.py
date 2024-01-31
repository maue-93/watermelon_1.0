from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action

from .models import Project, UserAccess, AccessRequest, RemovalRequest, Progress, Session, Topic, TopicInProject, Task
from .serializers import ProjectSerializer, UserAccessSerializer, AccessRequestSerializer, RemovalRequestSerializer, \
                        ProgressSerializer, SessionSerializer, TopicSerializer, TopicInProjectSerializer, TaskSerializer

# Create your views here.

"""
    last review : 01/09/2024 - by eliso morazara
    
    VIEWSET = ProjectViewSet : ViewSet for UserAccess

    USES :  1 - Access to the projects that this user is part of

    WHY :   1 - This helps organize our UI

    HOW IT WORKS :
            1 - We will use it to generate the posts for the user's feed, 

    NOTICE: 1 - Use filter to show only the projects that the user is part of

    TO DO : 1 - Override create method to create a user access when creating a project
            2 - Override create method to create a progress object when creating a project
            2 - Use filter to show only the projects that the user is part of
"""
class ProjectViewSet (ModelViewSet):
    def get_queryset(self):
        return Project.objects.prefetch_related('subprojects').all()
    def get_serializer_class(self):
        return ProjectSerializer
    
    def get_serializer_context(self):
        return {'user': self.request.user}
    
    # @action(detail=True, methods=['POST'])
    # def create_subproject(self, request, pk):
    #     current_project = self.get_object()
        
    #     return Response(ProjectSerializer(data=current_project))
# end of ProjectViewSet
    

"""
    last review : 01/09/2024 - by eliso morazara
    
    VIEWSET = UserAccessViewSet : ViewSet for UserAccess

    USES :  1 - Get user accesses of a user

    WHY :   1 - It is important to know what projects the user is part of at beginning, after they signed in

    HOW IT WORKS :
            1 - We will use this after someone signs in so we can show them their feed, and project list

    NOTICE: 1 - 

    TO DO : 1 - Use filter to show only the user accesses that the user has

"""
class UserAccessViewSet (ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    def get_queryset(self):
        return UserAccess.objects.select_related('project').all()
    def get_serializer_class(self):
        return UserAccessSerializer
# end of UserAccessViewSet


"""
    last review : 01/09/2024 - by eliso morazara
    
    VIEWSET = AccessRequestViewSet : ViewSet for AccessRequest

    USES :  1 - Get AccessRequest of a user 

    WHY :   1 - The app should have a section for invites and requests so the user can accept invite and see other
                associate's votes on the invite or request

    HOW IT WORKS :
            1 - The list of AccessRequest is usseful for display and we use POST, DELETE to creacte or delete a AccessRequest

    NOTICE: 1 - 

    TO DO : 1 - Use filter to show only the AccessRequest that the user is part of, including the ones they are neither
                invitor nor invitee but are part of the project concerned

"""
class AccessRequestViewSet (ModelViewSet):
    def get_queryset(self):
        return AccessRequest.objects.all()
    def get_serializer_class(self):
        return AccessRequestSerializer
# end of AccessRequestViewSet
    

"""
    last review : 01/09/2024 - by eliso morazara
    
    VIEWSET = RemovalRequestViewSet : ViewSet for RemovalRequest

    USES :  1 - Get RemovalRequest that a user is either the requester, the user to remove, or part of the project in question

    WHY :   1 - A user should vote or see how the vote of the RemovalRequest is going if they are part of the project

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - Use filter to show only the RemovalRequest that the user is part of or of which project they are part of
            2 - Make sure to force the fact that both user accesses needs to be of the same project

"""
class RemovalRequestViewSet (ModelViewSet):
    def get_queryset(self):
        return RemovalRequest.objects.all()
    def get_serializer_class(self):
        return RemovalRequestSerializer
# end of RemovalRequestViewSet


"""
    last review : 01/09/2024 - by eliso morazara
    
    VIEWSET = ProgressViewSet : ViewSet for Progress

    USES :  1 - See the progress of a project

    WHY :   1 - Visualizing how a project is moving shoud be a motivation to work harder

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - the detail should be a sub router of the projects/<pk>

"""
class ProgressViewSet (ModelViewSet):
    def get_queryset(self):
        return Progress.objects.all()
    def get_serializer_class(self):
        return ProgressSerializer
# end of ProgressViewSet
    

"""
    last review : 01/09/2024 - by eliso morazara
    
    VIEWSET = SessionViewSet : ViewSet for Session

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 

"""
class SessionViewSet (ModelViewSet):
    def get_queryset(self):
        return Session.objects.all()
    def get_serializer_class(self):
        return SessionSerializer
# end of SessionViewSet


"""
    last review : 01/10/2024 - by eliso morazara
    
    VIEWSET = TopicViewSet : ViewSet for Topic

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 

"""
class TopicViewSet (ModelViewSet):
    def get_queryset(self):
        return Topic.objects.all()
    def get_serializer_class(self):
        return TopicSerializer
# end of TopicViewSet


"""
    last review : 01/11/2024 - by eliso morazara
    
    VIEWSET = TopicHierarchyViewSet : ViewSet for TopicHierarchy

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 

"""
class TopicInProjectViewSet (ModelViewSet):
    def get_queryset(self):
        return TopicInProject.objects.all()
    def get_serializer_class(self):
        return TopicInProjectSerializer
# end of TopicHierarchyViewSet


"""
    last review : 01/11/2024 - by eliso morazara
    
    VIEWSET = TaskViewSet : ViewSet for Task

    USES :  1 - 

    WHY :   1 - 

    HOW IT WORKS :
            1 - 

    NOTICE: 1 - 

    TO DO : 1 - 

"""
class TaskViewSet (ModelViewSet):
    def get_queryset(self):
        return Task.objects.all()
    def get_serializer_class(self):
        return TaskSerializer
# end of TaskViewSet




