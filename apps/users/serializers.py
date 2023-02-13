from rest_framework import serializers

from apps.projects.models import ProjectUser
from apps.users.models import UserProfile


class SignupSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'avatar', 'mobile')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = UserProfile.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=False)
    projects = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'mobile',
            'projects'
        )
        read_only_fields = ('id', 'username')

    def get_projects(self, instance):
        active_projects = ProjectUser.objects.filter(assign_to=instance.id).values_list(
            'project__id', flat=True
        ).count()
        return active_projects