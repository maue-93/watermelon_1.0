from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('reactions', views.ReactionViewSet, basename='reactions')
router.register('votes', views.VoteViewSet, basename='votes')
router.register('vouches', views.VouchViewSet, basename='vouches')
router.register('tags', views.TagViewSet, basename='tags')

urlpatterns = [
    path(r'', include(router.urls)),
]