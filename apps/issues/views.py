import logging
from rest_framework.permissions import IsAuthenticated

from apps.issues.models import Issues
from apps.issues.serializers import IssueSerializer, IssueUserSerializer

from manager_project.core.views import BaseViewSet
from rest_framework import mixins, status

logger = logging.getLogger(__name__)


# Create your views here.
class IssueViewSet(
    BaseViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin
):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Issues.objects.all()
        return Issues.objects.filter(project=self.request.query_params.get('project'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "issue_users": self.request.data.get('issue_users'),
                "request": self.request,
            }
        )
        return context

