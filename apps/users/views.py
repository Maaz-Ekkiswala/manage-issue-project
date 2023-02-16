from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users import filters
from apps.users.models import UserProfile
from apps.users.serializers import SignupSerializer, UserProfileSerializer


# Create your views here.


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Invalid data '{}'".format(serializer.errors)},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_profile = serializer.save()
        ser = TokenObtainPairSerializer(data=serializer.validated_data)
        ser.is_valid()
        return Response({
            "user": UserProfileSerializer(instance=user_profile).data,
            **ser.validated_data
        })


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

