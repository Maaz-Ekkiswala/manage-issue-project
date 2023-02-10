import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.issues.functions import is_project_user
from apps.issues.models import Issues, IssueUser
from apps.issues.serializers import IssueSerializer

from manager_project.core.views import BaseViewSet
from rest_framework import mixins, status

logger = logging.getLogger(__name__)


# Create your views here.
class IssueViewSet(
    BaseViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin
):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Issues.objects.all()
        return Issues.objects.filter(project_id=self.request.query_params.get('project_id'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "issue_users": self.request.data.get('issue_users'),
                "request": self.request,
            }
        )
        return context

    @action(
        detail=True, methods=['post', 'put'], url_name='issue_users',
        url_path='issue-users'
    )
    def issue_users(self, request, pk):
        try:
            issue_instance = Issues.objects.get(pk=pk)
            issue_users = request.data.get('assign_to')
            project_user = is_project_user(
                project_id=issue_instance.project,
                users=issue_users,
                logged_in_user=self.request.user
            )
            if project_user:
                if self.request.stream.method == 'POST':
                    issue_users_list = []
                    for issue_user in issue_users:
                        issue_users_list.append(
                            IssueUser(issue=issue_instance, assign_to_id=issue_user)
                        )
                    if issue_users_list:
                        IssueUser.objects.bulk_create(issue_users_list)
                    return Response(
                        IssueSerializer(instance=issue_instance).data,
                        status=status.HTTP_201_CREATED
                    )
                if self.request.stream.method == 'PUT':
                    issue_users_list = []
                    IssueUser.objects.filter(issue=issue_instance).delete()
                    for issue_user in issue_users:
                        issue_users_list.append(
                            IssueUser(issue=issue_instance, assign_to_id=issue_user)
                        )
                    if issue_users_list:
                        IssueUser.objects.bulk_create(issue_users_list)
                    return Response(
                        IssueSerializer(instance=issue_instance).data,
                        status=status.HTTP_200_OK
                    )
                return Response({
                    "message": "You cannot assign user which are not in project"
                }, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({
                "message": "Issue not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(
        detail=True, methods=['delete'], url_name='issue_users',
        url_path='issue-users/(?P<user_id>[0-9]*)'
    )
    def delete_project_users(self, request, user_id, pk):
        try:
            issue_instance = Issues.objects.get(pk=pk)
            issue_user = IssueUser.objects.filter(
                issue=issue_instance,
                assign_to=user_id
            )
            if not issue_user:
                return Response({
                    "message": "Issue user not found"
                }, status=status.HTTP_404_NOT_FOUND)
            issue_user.delete()
            return Response(
                {"message": "Issue user deleted successfully"},
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response({
                "message": "Issue not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)