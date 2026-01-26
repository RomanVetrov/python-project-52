from django import forms

from .models import Label


class LabelForm(forms.ModelForm):
    """Форма создания и редактирования меток."""
    class Meta:
        model = Label
        fields = ("name",)
