from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet, basename='collections')

urlpatterns = [
    path(r'', include(router.urls)),
]


