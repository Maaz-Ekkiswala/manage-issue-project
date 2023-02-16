from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.issues import views

issue_router = DefaultRouter()
issue_router.register(r'', views.IssueViewSet, 'issues')

urlpatterns = [
    path('', include(issue_router.urls)),
]