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
        user = UserProfile.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data['avatar'],
            mobile=validated_data['mobile']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=False)
    active_projects = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'mobile',
            'active_projects'
        )
        read_only_fields = ('id', 'username')

    def get_active_projects(self, instance):
        project_ids = ProjectUser.objects.filter(assign_to=instance.id).values_list(
            'project__id', flat=True
        )
        active_projects = len(project_ids)
        return active_projects