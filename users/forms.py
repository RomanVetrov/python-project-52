from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserUpdateForm(UserChangeForm):
    password = None  # убираем поле password из формы

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
