from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions

from apps.users import filters
from apps.users.models import UserProfile
from apps.users.serializers import SignupSerializer, UserProfileSerializer


# Create your views here.


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignupSerializer


class UserViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    serializer_class = UserProfileSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.UserFilterSet

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(pk=self.request.user.id)

    def get_permissions(self):
        perm_classes = [permissions.IsAuthenticated]
        if self.action in ['retrieve', 'update']:
            return [permission() for permission in perm_classes]
        if self.action == 'list':
            perm_classes.append(permissions.IsAdminUser)
        return [permission() for permission in perm_classes]

