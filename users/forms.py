from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")


class UserUpdateForm(UserChangeForm):
    """Форма изменения профиля с необязательной сменой пароля."""

    password = None  # скрываем readonly пароль из родителя
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        required=False,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Пароли не совпадают")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
