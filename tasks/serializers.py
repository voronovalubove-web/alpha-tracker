from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project, Task

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    '''Сериализатор для Project с вложенным отображением участников.'''
    members = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=User.objects.all(),
        required=False,
        default=[]
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'members']
        read_only_fields = ['id', 'owner']


class TaskSerializer(serializers.ModelSerializer):
    '''Сериализатор для Task с валидацией, что assignee является участником проекта.'''
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        required=False, 
        allow_null=True
    )
    
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all()
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 
            'status', 'deadline', 'author', 'assignee', 'project'
        ]
        read_only_fields = ['id', 'author']

    def validate(self, data):
        '''Проверка, что назначенный исполнитель является участником проекта.'''
        assignee = data.get('assignee') 
        
        project = data.get('project') or getattr(self.instance, 'project', None)

        if assignee and project:
            if not project.members.filter(id=assignee.id).exists():
                raise serializers.ValidationError({
                    "assignee": "Назначенный исполнитель не является участником проекта."
                })
        return data