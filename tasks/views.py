from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.utils.translation import gettext_lazy as _

from core.mixins import LoginRequiredMessageMixin

from .forms import TaskForm, TaskFilterForm
from .models import Task


class TaskListView(LoginRequiredMessageMixin, ListView):
    """Список задач; виден только авторизованным пользователям."""
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("status", "author", "executor")
            .prefetch_related("labels")
        )

        form = TaskFilterForm(self.request.GET or None)
        if form.is_valid():
            if form.cleaned_data.get("status"):
                queryset = queryset.filter(status=form.cleaned_data["status"])
            if form.cleaned_data.get("executor"):
                queryset = queryset.filter(executor=form.cleaned_data["executor"])
            if form.cleaned_data.get("labels"):
                queryset = queryset.filter(labels=form.cleaned_data["labels"])
            if form.cleaned_data.get("self_tasks"):
                queryset = queryset.filter(author=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = TaskFilterForm(self.request.GET or None)
        return context


class TaskDetailView(LoginRequiredMessageMixin, DetailView):
    """Карточка задачи с подробностями."""
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMessageMixin, CreateView):
    """Создание задачи; автор проставляется автоматически."""
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Задача успешно создана"))
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMessageMixin, UpdateView):
    """Редактирование задачи."""
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        messages.success(self.request, _("Задача успешно изменена"))
        return super().form_valid(form)


class OnlyAuthorDeleteMixin(UserPassesTestMixin):
    """Миксин разрешает удаление задачи только её автору."""
    def test_func(self):
        return self.get_object().author_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, _("Только автор задачи может удалить её"))
        return redirect(reverse_lazy("tasks:list"))


class TaskDeleteView(LoginRequiredMessageMixin, OnlyAuthorDeleteMixin, DeleteView):
    """Удаление задачи; авторизация и проверка авторства обязательны."""
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return LoginRequiredMessageMixin.handle_no_permission(self)

        messages.error(self.request, _("Только автор задачи может удалить её"))
        return redirect(reverse_lazy("tasks:list"))

    def form_valid(self, form):
        messages.success(self.request, _("Задача успешно удалена"))
        return super().form_valid(form)
