from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """Тег для группировки задач; используется в связи многие-ко-многим."""

    name = models.CharField(_("Name"), max_length=255, unique=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return self.name
