from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status
from .models import Task


class TaskForm(forms.ModelForm):
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
