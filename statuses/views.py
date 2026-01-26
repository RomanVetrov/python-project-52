from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.utils.translation import gettext_lazy as _

from core.mixins import LoginRequiredMessageMixin

from .forms import StatusForm
from .models import Status

STATUSES_LIST_URL = "statuses:list"


class StatusListView(LoginRequiredMessageMixin, ListView):
    """Список статусов; доступен только авторизованным."""
    model = Status
    template_name = "statuses/list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMessageMixin, CreateView):
    """Создание статуса."""
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy(STATUSES_LIST_URL)

    def form_valid(self, form):
        messages.success(self.request, _("Статус успешно создан"))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMessageMixin, UpdateView):
    """Редактирование существующего статуса."""
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy(STATUSES_LIST_URL)

    def form_valid(self, form):
        messages.success(self.request, _("Статус успешно изменен"))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMessageMixin, DeleteView):
    """Удаление статуса с проверкой на использование в задачах."""
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy(STATUSES_LIST_URL)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                _("Невозможно удалить статус, потому что он используется"),
            )
            return redirect(STATUSES_LIST_URL)

        messages.success(self.request, _("Статус успешно удален"))
        return response
