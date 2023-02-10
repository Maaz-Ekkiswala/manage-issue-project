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
        detail=True, methods=['post', 'put'], url_name='project_users',
        url_path='project-users'
    )
    def project_users(self, request, pk):
        try:
            project_instance = Project.objects.get(pk=pk)
            list_data = [{'project': project_instance.id, **item} for item in request.data]
            serializer = ProjectUserSerializer(data=list_data, many=True)
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
            if self.request.stream.method == 'PUT':
                ProjectUser.objects.filter(project=project_instance).delete()
                if not serializer.is_valid():
                    return Response({
                        "message": "Invalid Data {}".format(serializer.errors)
                    }, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(
                    ProjectDetailedSerializer(instance=project_instance).data,
                    status=status.HTTP_200_OK
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

    @action(
        detail=True, methods=['delete'], url_name='project_users',
        url_path='project-users/(?P<user_id>[0-9]*)'
    )
    def delete_project_users(self, request, user_id, pk):
        try:
            project_instance = Project.objects.get(pk=pk)
            project_user = ProjectUser.objects.filter(project=project_instance, assign_to=user_id)
            if not project_user:
                return Response({
                    "message": "Project user not found"
                }, status=status.HTTP_404_NOT_FOUND)
            project_user.delete()
            return Response(
                {"message": "Project user deleted successfully"},
                status=status.HTTP_200_OK
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



# class ProjectUserViewSet(BaseViewSet, mixins.CreateModelMixin):
#     serializer_class = ProjectUserSerializer
#     queryset = ProjectUsers.objects.all()
#
#     def get_permissions(self):
#         perm_classes = [permissions.IsAuthenticated]
#         if self.action in ['create', 'update', 'list']:
#             perm_classes.append(permissions.IsAdminUser)
#         return [permission() for permission in perm_classes]
#
#     def create(self, request, pk=None, *args, **kwargs):
#         try:
#             project_instance = Project.objects.get(pk=pk)
#             if not project_instance:
#                 return Response({
#                     "message": "Project not found"
#                 }, status=status.HTTP_404_NOT_FOUND)
#             list_data = [{'project': project_instance.id, **item} for item in request.data]
#             serializer = self.serializer_class(data=list_data, many=True)
#             if not serializer.is_valid():
#                 return Response({
#                     "message": "Invalid Data {}".format(serializer.errors)
#                 }, status=status.HTTP_400_BAD_REQUEST)
#             serializer.save(created_by=self.request.user)
#             return Response(
#                 ProjectDetailedSerializer(instance=project_instance).data,
#                 status=status.HTTP_201_CREATED
#             )
#         except Exception as ex:
#             return Response({
#                 "message": "Something went wrong '{}'".format(ex)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)