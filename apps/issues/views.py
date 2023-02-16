import logging

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.issues import filters
from apps.issues.models import Issues, IssueUser
from apps.issues.serializers import IssueSerializer
from manager_project.core.permissions import ProjectUserPermission

from manager_project.core.views import BaseViewSet
from rest_framework import status, permissions, viewsets

logger = logging.getLogger(__name__)


# Create your views here.
class IssueViewSet(BaseViewSet, viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.IssueFilterSet

    def get_permissions(self):
        perm_classes = [permissions.IsAuthenticated]
        if self.action in ['create', 'update', 'list', 'retrieve', 'issue_users', 'destroy']:
            perm_classes.append(permissions.IsAdminUser | ProjectUserPermission)
        return [permission() for permission in perm_classes]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Issues.objects.all()
        if self.request.query_params.get('project_id'):
            queryset = Issues.objects.filter(
                project_id=self.request.query_params.get('project_id')
            )
            if self.request.query_params.get('only_my_issues'):
                queryset = queryset.filter(issue_users__assign_to=self.request.user)
            if self.request.query_params.get('issue_user_ids__in'):
                issue_user_ids = self.request.query_params.get('issue_user_ids__in').split(',')
                queryset = queryset.filter(
                    issue_users__assign_to_id__in=issue_user_ids
                )
            return queryset
        return Issues.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "issue_users": self.request.data.get('issue_users'),
                "request": self.request,
            }
        )
        return context

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            issue_instance = Issues.objects.get(pk=pk)
            return Response(IssueSerializer(instance=issue_instance).data)
        except ObjectDoesNotExist:
            return Response({
                "message": "Issue not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            issue_instance = Issues.objects.get(pk=pk)
            if issue_instance.created_by != self.request.user:
                return Response(
                    {"message": "You cannot delete other's issue"},
                    status=status.HTTP_403_FORBIDDEN
                )
            issue_instance.delete()
            return Response({"message": "Issue deleted successfully"})
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
        detail=True, methods=['post'], url_name='issue_users',
        url_path='issue-users'
    )
    def issue_users(self, request, pk):
        try:
            issue_instance = Issues.objects.get(pk=pk)
            issue_users = request.data.get('issue_users')
            if not issue_users:
                return Response({
                    "message": "You should assign atleast one user in issue"
                }, status=status.HTTP_400_BAD_REQUEST)
            if self.request.stream.method == 'POST':
                issue_users_list = []
                for issue_user in issue_users:
                    issue_users_list.append(
                        IssueUser(issue=issue_instance, assign_to_id=issue_user)
                    )
                IssueUser.objects.filter(issue=issue_instance).delete()
                if issue_users_list:
                    IssueUser.objects.bulk_create(issue_users_list)
                return Response(
                    IssueSerializer(instance=issue_instance).data,
                    status=status.HTTP_201_CREATED
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
