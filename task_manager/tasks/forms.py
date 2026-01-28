from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_("Executor"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем ФИО в выпадающем списке исполнителей
        self.fields["executor"].label_from_instance = (
            lambda u: f"{u.first_name} {u.last_name}".strip() or u.username
        )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label=_("Status"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_("Executor"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    labels = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_("Label"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    self_tasks = forms.BooleanField(
        required=False,
        label=_("Only my tasks"),
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )  # фильтр по автору

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].label_from_instance = (
            lambda u: f"{u.first_name} {u.last_name}".strip() or u.username
        )
