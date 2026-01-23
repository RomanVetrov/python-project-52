from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from statuses.models import Status


class Task(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name=_("Status"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        verbose_name=_("Author"),
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="executed_tasks",
        null=True,
        blank=True,
        verbose_name=_("Executor"),
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return self.name
