from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.projects import views

project_router = DefaultRouter()


project_router.register(r'', views.ProjectViewSet, 'project')

urlpatterns = [
    path('', include(project_router.urls)),
]