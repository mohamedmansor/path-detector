from django.urls import path, include
from rest_framework.routers import DefaultRouter

from node import views

router = DefaultRouter(trailing_slash=False)

router.register(r'connectNode', views.ConnectNodesViewSet, basename='connectNode')
router.register(r'', views.PathViewSet, basename='')

urlpatterns = [
    path('', include(router.urls)),
]
