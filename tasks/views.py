from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from rest_framework import viewsets, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permissions import ProjectTaskPermission

User = get_user_model()

class CurrentUserView(APIView):
    """Возвращает данные текущего авторизованного пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'username': request.user.username,
            'id': request.user.id
        })


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectTaskPermission]
    filterset_fields = ['name']

    def get_queryset(self):
        """пользователь видит только свои проекты или те, где он участник"""
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        """Автоматически назначаем текущего пользователя владельцем"""
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectTaskPermission]
    filterset_fields = ['project', 'status', 'priority', 'assignee', 'deadline']

    def get_queryset(self):
        """задачи видны только из проектов, где пользователь состоит"""
        user = self.request.user
        return Task.objects.filter(
            Q(project__owner=user) | Q(project__members=user)
        ).distinct()

    def perform_create(self, serializer):
        """Проверяем доступ к проекту перед созданием задачи"""
        project_id = self.request.data.get('project')
        if project_id:
            get_object_or_404(
                Project.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user)),
                id=project_id
            )
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Ограничиваем редактируемые поля в зависимости от роли"""
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
        serializer.save(**filtered_data)


def test_ui(request):
    """Отдает простой HTML-интерфейс для ручной проверки API"""
    return render(request, 'tasks/test_ui.html')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]