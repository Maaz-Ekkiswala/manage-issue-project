from django.urls import path, include
from rest_framework.routers import DefaultRouter


from apps.users import views

auth_router = DefaultRouter()
auth_router.register(r'', views.SignUpViewSet, 'user-auth')

user_router = DefaultRouter()
user_router.register(r'', views.UserViewSet, 'user')

urlpatterns = [
    path('signup/', include(auth_router.urls)),
    path('', include(user_router.urls))
]