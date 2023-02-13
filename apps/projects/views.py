import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status, permissions
from rest_framework.decorators import action

from rest_framework.response import Response

from apps.projects.models import Project, ProjectUser
from apps.projects.serializers import (
    ProjectSerializer, ProjectDetailedSerializer, ProjectUserSerializer
)
from manager_project.core.views import BaseViewSet

logger = logging.getLogger(__name__)


# Create your views here.
class ProjectViewSet(
    BaseViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin
):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_permissions(self):
        perm_classes = [permissions.IsAuthenticated]
        if self.action in ['create', 'update', 'list']:
            perm_classes.append(permissions.IsAdminUser)
        return [permission() for permission in perm_classes]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "message": "Invalid Data {}".format(serializer.errors)
                }, status=status.HTTP_400_BAD_REQUEST)
            project = serializer.save(created_by=self.request.user)
            return Response(
                ProjectDetailedSerializer(instance=project).data, status=status.HTTP_201_CREATED
            )
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            project = Project.all_objects.filter(id=pk).first()
            if not project.is_active:
                return Response({
                    "message": "Project is inactive",
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(ProjectDetailedSerializer(instance=project).data)
        except ObjectDoesNotExist:
            return Response({
                "message": "Project not found",
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(
        detail=True, methods=['post'], url_name='project_users',
        url_path='project-users'
    )
    def project_users(self, request, pk):
        try:
            project_instance = Project.objects.get(pk=pk)
            project_users_data_list = [{'project': project_instance.id, **item} for item in request.data]
            serializer = ProjectUserSerializer(data=project_users_data_list, many=True)
            if self.request.stream.method == 'POST':
                if not serializer.is_valid():
                    return Response({
                        "message": "Invalid Data {}".format(serializer.errors)
                    }, status=status.HTTP_400_BAD_REQUEST)

                serializer.save(created_by=self.request.user)
                return Response(
                    ProjectDetailedSerializer(instance=project_instance).data,
                    status=status.HTTP_201_CREATED
                )
        except ObjectDoesNotExist:
            return Response({
                "message": "Project not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response({
                "message": "Something went wrong '{}'".format(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
