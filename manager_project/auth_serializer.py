from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import UserProfileSerializer


class ManagerProjectObtainPairSerializer(serializers.TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        try:
            user_profile_instance = UserProfileSerializer(instance=self.user).data
            data['user_profile'] = user_profile_instance
            return data
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"error": "You are not allowed to sign-in in this portal."})


class ManagerProjectObtainPairView(TokenObtainPairView):
    serializer_class = ManagerProjectObtainPairSerializer