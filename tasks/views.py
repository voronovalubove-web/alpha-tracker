from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer
from .filters import TaskFilter
from .permissions import ProjectTaskPermission

User = get_user_model()

class CurrentUserView(APIView):
    '''Простой эндпоинт для получения данных текущего пользователя.'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'username': request.user.username, 'id': request.user.id})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''Эндпоинт для просмотра списка пользователей (для выбора в проектах/задачах).'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    '''Эндпоинт для управления проектами. Владелец проекта может делать всё,
     участники могут только читать.'''
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectTaskPermission]

    def get_queryset(self):
        user = self.request.user
        return (
            Project.objects.filter(owner=user) | Project.objects.filter(members=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    '''Эндпоинт для управления задачами. Владелец проекта может делать всё,
     автор и исполнитель могут менять статус/приоритет, автор может менять описание, автор может удалять.'''
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ProjectTaskPermission]
    filterset_class = TaskFilter

    def get_queryset(self):
        user = self.request.user
        return (
            Task.objects.filter(project__owner=user) | Task.objects.filter(project__members=user)
        ).distinct()

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        if not project_id:
            raise serializers.ValidationError({"project": "Укажите проект."})

        get_object_or_404(
            Project.objects.filter(owner=self.request.user) | Project.objects.filter(members=self.request.user),
            id=project_id
        )
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        task = self.get_object()

        if user == task.project.owner:
            serializer.save()
            return

        allowed_fields = set()
        if user == task.assignee:
            allowed_fields.update({'status', 'priority'})
        if user == task.author:
            allowed_fields.add('description')

        filtered_data = {k: v for k, v in serializer.validated_data.items() if k in allowed_fields}
        if not filtered_data:
            raise PermissionDenied("Недостаточно прав для изменения этих полей.")

        serializer.save(**filtered_data)