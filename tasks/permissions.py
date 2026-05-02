from rest_framework import permissions
from .models import Project, Task

class ProjectTaskPermission(permissions.BasePermission):
    """Права доступа для задач"""
    def has_object_permission(self, request, view, obj):
        user = request.user
        action = getattr(view, 'action', None)

        if action in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Project):
            return user == obj.owner

        project_owner = obj.project.owner
        if user == project_owner:
            return True  

        if action == 'destroy':
            return user == obj.author  

        if action in ('update', 'partial_update'):
            return user == obj.assignee or user == obj.author  

        return False