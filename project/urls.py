from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


"""
    last review : 01/09/2024 - by eliso morazara
    
    TO DO : 1 - FIGURE OUT THE REAL MEANING OF BASENAME IN REGISTER

    ENDPOINTS:
        - user_accesses/ : list of all the active accesses the user has
            - user_accesses/<id>/ : one access to a project
        - projects/ : list of all projects this user is part of
            - projects/<id>/ : one project
        - access_requests/ : list of all access requests that concerns the user
            - access_requests/<id> : one access request
        - removal_requests/ : list of all removal requests that concerns the user
            - removal_requests/<id> : one removal request
        - progresses/ : list of all project progresses
            - progresses/<id> : one project progress
        - 
"""

router = routers.DefaultRouter()
router.register('user_accesses', views.UserAccessViewSet, basename='user_accesses')
router.register('projects', views.ProjectViewSet, basename='projects')
router.register('access_requests', views.AccessRequestViewSet, basename='access_requests')
router.register('removal_requests', views.RemovalRequestViewSet, basename='removal_requests')
router.register('progresses', views.ProgressViewSet, basename='progresses')
router.register('sessions', views.SessionViewSet, basename='sessions')
router.register('topics', views.TopicViewSet, basename='topics')
router.register('topics_in_projects', views.TopicInProjectViewSet, basename='topics_in_projects')
router.register('tasks', views.TaskViewSet, basename='tasks')


urlpatterns = [
    path(r'', include(router.urls)),
]