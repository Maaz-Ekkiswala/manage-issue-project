from apps.comments.models import Comments
from manager_project.core.serializers import BaseSerializer


class CommentSerializer(BaseSerializer):

    class Meta:
        model = Comments
        fields = ("id", "issue", "commented_by", "description")
        read_only_fields = ("id", "issue", "commented_by")

