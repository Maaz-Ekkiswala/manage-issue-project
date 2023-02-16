from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.comments import views

comment_router = DefaultRouter()
comment_router.register(r'', views.CommentViewSet, 'comments')

urlpatterns = [
    path('', include(comment_router.urls)),
]