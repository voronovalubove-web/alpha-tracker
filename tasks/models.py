from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    name = models.CharField(_('название'), max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name=_('владелец')
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='member_projects',
        blank=True,
        verbose_name=_('участники')
    )

    class Meta:
        verbose_name = _('проект')
        verbose_name_plural = _('проекты')
        ordering = ['-id']

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'low', _('Низкий')
        MEDIUM = 'medium', _('Средний')
        HIGH = 'high', _('Высокий')
        URGENT = 'urgent', _('Срочный')

    class Status(models.TextChoices):
        NEW = 'new', _('Новая')
        IN_PROGRESS = 'in_progress', _('В работе')
        DONE = 'done', _('Готова')
        CLOSED = 'closed', _('Закрыта')

    title = models.CharField(_('заголовок'), max_length=150)
    description = models.TextField(_('описание'), blank=True, default='')
    priority = models.CharField(
        _('приоритет'), max_length=10,
        choices=Priority.choices, default=Priority.MEDIUM
    )
    status = models.CharField(
        _('статус'), max_length=15,
        choices=Status.choices, default=Status.NEW
    )
    deadline = models.DateField(_('дедлайн'), null=True, blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
        verbose_name=_('автор')
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=_('исполнитель')
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('проект')
    )

    class Meta:
        verbose_name = _('задача')
        verbose_name_plural = _('задачи')
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"