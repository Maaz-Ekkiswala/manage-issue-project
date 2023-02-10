"""manager_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt import views as jwt_views

from manager_project.auth_serializer import ManagerProjectObtainPairView

openapi_info = openapi.Info(
    title="Manger Project",
    default_version='v1',
    description="All the endpoints of the Manager Project backend",
    license=openapi.License(name="All Rights Reserved"),
)

schema_view = get_schema_view(
    openapi_info,
    public=True,
)
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/v1/users/', include(('apps.users.urls', "users"), namespace="users")),
    path('api/v1/masters/', include(('apps.masters.urls', "masters"), namespace="masters")),
    path('api/v1/projects/', include(('apps.projects.urls', "projects"), namespace="projects")),
    path('api/v1/issues/', include(('apps.issues.urls', "issues"), namespace="issues")),

    # JWT urls
    path('api/v1/login/', ManagerProjectObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
