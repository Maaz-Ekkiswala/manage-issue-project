from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.masters import views

master_router = DefaultRouter()

master_router.register(r'category', views.CategoryViewSet, 'category')

urlpatterns = [
    path('', include(master_router.urls)),
]