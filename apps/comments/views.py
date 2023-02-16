import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status, permissions
from rest_framework.response import Response

from apps.comments.models import Comments
from apps.comments.serializers import CommentSerializer
from manager_project.core.permissions import IssueUserPermission
from manager_project.core.views import BaseViewSet

# Create your views here.
logger = logging.getLogger(__name__)


class CommentViewSet(
    BaseViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.request.query_params.get('issue_id'):
            return Comments.objects.filter(issue_id=self.request.query_params.get('issue_id'))
        return Comments.objects.none()

    def get_permissions(self):
        perm_classes = [permissions.IsAuthenticated]
        if self.action in ['create', 'update', 'list', 'destroy']:
            perm_classes.append(permissions.IsAdminUser | IssueUserPermission)
        return [permission() for permission in perm_classes]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "message": "Invalid Data {}".format(serializer.errors)
                }, status=status.HTTP_400_BAD_REQUEST)
            issue_id = self.request.query_params.get('issue_id')
            if issue_id:
                comment_instance = serializer.save(
                    issue_id=issue_id,
                    created_by=self.request.user,
                    commented_by_id=self.request.user.id
                )
                return Response(
                    CommentSerializer(instance=comment_instance).data, status=status.HTTP_201_CREATED
                )
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            comment_instance = Comments.objects.get(pk=pk)
            if comment_instance.commented_by.id != self.request.user.id:
                return Response(
                    {"message": "You cannot update other's comment"},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.serializer_class(instance=comment_instance, data=request.data)
            if not serializer.is_valid():
                if not serializer.is_valid():
                    return Response({
                        "message": "Invalid Data {}".format(serializer.errors)
                    }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(update_by=self.request.user)
            return Response(CommentSerializer(instance=comment_instance).data)
        except ObjectDoesNotExist:
            return Response({
                "message": "Comment not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            comment_instance = Comments.objects.get(pk=pk)
            if comment_instance.commented_by.id != self.request.user.id:
                return Response(
                    {"message": "You cannot delete other's comment"},
                    status=status.HTTP_403_FORBIDDEN
                )
            comment_instance.delete()
            return Response({"message": "Comment deleted successfully"})
        except ObjectDoesNotExist:
            return Response({
                "message": "Comment not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)