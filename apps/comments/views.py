import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.comments.functions import is_issue_user
from apps.comments.models import Comments
from apps.comments.serializers import CommentSerializer, CommentUpdateSerializer
from manager_project.core.views import BaseViewSet

# Create your views here.
logger = logging.getLogger(__name__)


class CommentViewSet(
    BaseViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.request.query_params.get('issue_id'))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "message": "Invalid Data {}".format(serializer.errors)
                }, status=status.HTTP_400_BAD_REQUEST)
            issue_id = serializer.validated_data.get('issue')
            issue_user = is_issue_user(issue_id=issue_id, logged_in_user=self.request.user)
            if issue_user:
                comment_instance = serializer.save(created_by=self.request.user, commented_by_id=self.request.user.id)
                return Response(
                    CommentSerializer(instance=comment_instance).data, status=status.HTTP_201_CREATED
                )
            return Response(
                {"message": "You are not allowed to comment on this issue"},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            comment_instance = Comments.objects.get(pk=pk)
            if comment_instance.commented_by != self.request.user:
                return Response(
                    {"message": "You cannot update other's comment"},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = CommentUpdateSerializer(instance=comment_instance, data=request.data)
            if not serializer.is_valid():
                if not serializer.is_valid():
                    return Response({
                        "message": "Invalid Data {}".format(serializer.errors)
                    }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
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
            if comment_instance.commented_by != self.request.user:
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