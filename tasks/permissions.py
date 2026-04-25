from rest_framework import permissions

class ProjectTaskPermission(permissions.BasePermission):
    """
    Контроль доступа на уровне объектов:
    - Владелец проекта: полный доступ
    - Исполнитель задачи: обновление статуса и приоритетаs
    - Автор задачи: обновление описания, удаление
    - Остальные участники проекта: только чтение
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        action = getattr(view, 'action', None)

        owner = getattr(obj, 'owner', None) or getattr(getattr(obj, 'project', None), 'owner', None)

        if user == owner:
            return True

        if action in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'project'):
            is_member = obj.project.members.filter(id=user.id).exists()
            if not is_member:
                return False

            if action == 'destroy':
                return user == obj.author

            if action in ('update', 'partial_update'):
                return user == obj.assignee or user == obj.author

        return False