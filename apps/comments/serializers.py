from rest_framework.exceptions import ValidationError

from apps.comments.functions import is_issue_user
from apps.comments.models import Comments
from manager_project.core.serializers import BaseSerializer


class CommentSerializer(BaseSerializer):

    class Meta:
        model = Comments
        fields = ("id", "issue", "commented_by", "description")
        read_only_fields = ("id", "commented_by")


class CommentUpdateSerializer(BaseSerializer):

    class Meta:
        model = Comments
        fields = ("id", "issue", "commented_by", "description")
        read_only_fields = ("id", "issue", "commented_by")

    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     issue_user = is_issue_user(issue_id=instance.issue, logged_in_user=request.user)
    #     if not issue_user:
    #         raise ValidationError({"error": "You are not allowed to update other's comment"})
    #     super().update(instance, validated_data)
    #     return instance
