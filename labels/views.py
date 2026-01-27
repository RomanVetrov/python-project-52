from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.utils.translation import gettext_lazy as _

from core.mixins import LoginRequiredMessageMixin

from .forms import LabelForm
from .models import Label

LABELS_LIST_URL = "labels:list"


class LabelListView(LoginRequiredMessageMixin, ListView):
    """Список меток."""
    model = Label
    template_name = "labels/list.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMessageMixin, CreateView):
    """Создание метки."""
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy(LABELS_LIST_URL)

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно создана"))
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMessageMixin, UpdateView):
    """Редактирование метки."""
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy(LABELS_LIST_URL)

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно изменена"))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMessageMixin, DeleteView):
    """Удаление метки; блокируем, если она используется задачами."""
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy(LABELS_LIST_URL)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(
                request,
                _("Невозможно удалить метку, потому что она используется"),
            )
            return redirect(LABELS_LIST_URL)

        messages.success(request, _("Метка успешно удалена"))
        return super().post(request, *args, **kwargs)
