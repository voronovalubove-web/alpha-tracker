import django_filters
from django.utils import timezone
from .models import Task


class TaskFilter(django_filters.FilterSet):
    '''фильтр для задач по дедлайну'''
    deadline__gte = django_filters.DateFilter(
        field_name='deadline',
        lookup_expr='gte',
        label='Deadline от (YYYY-MM-DD)'
    )
    deadline__lte = django_filters.DateFilter(
        field_name='deadline',
        lookup_expr='lte',
        label='Deadline до (YYYY-MM-DD)'
    )

    class Meta:
        '''фильтр для задач по проекту, статусу, приоритету, исполнителю и дедлайну'''
        model = Task
        fields = {
            'project': ['exact'],
            'status': ['exact'],
            'priority': ['exact'],
            'assignee': ['exact'],
            'deadline': ['exact', 'isnull'],
        }