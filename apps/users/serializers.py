from rest_framework import serializers

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

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'mobile'
        )
        read_only_fields = ('id', 'username')
