from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.utils.translation import gettext_lazy as _

from .forms import SignupForm, UserUpdateForm

USERS_LIST_URL = "users:list"


class UserListView(ListView):
    """Публичный список пользователей."""
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    """Регистрация нового пользователя."""
    model = User
    form_class = SignupForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")  # после регистрации на страницу входа

    def form_valid(self, form):
        messages.success(self.request, _("Пользователь успешно зарегистрирован"))
        return super().form_valid(form)


class OnlySelfMixin(UserPassesTestMixin):
    """Разрешает правку и удаление только владельцу аккаунта."""
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.pk == self.get_object().pk
        )

    def handle_no_permission(self):
        messages.error(
            self.request, _("У вас нет прав для изменения другого пользователя")
        )
        return redirect("users:list")


class UserUpdateView(OnlySelfMixin, UpdateView):
    """Редактирование собственного профиля."""
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy(USERS_LIST_URL)  # после изменения на список пользователей

    def form_valid(self, form):
        messages.success(self.request, _("Пользователь успешно изменен"))
        return super().form_valid(form)


class UserDeleteView(OnlySelfMixin, DeleteView):
    """Удаление собственного аккаунта; блокируется, если есть связанные задачи."""
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy(USERS_LIST_URL)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                _("Невозможно удалить пользователя, потому что он используется"),
            )
            return redirect("users:list")

        messages.success(self.request, _("Пользователь успешно удален"))
        return response


class UserLoginView(LoginView):
    """Форма входа с редиректом на главную после успеха."""
    template_name = "users/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Вы залогинены"))
        return response

    def get_success_url(self):
        return reverse_lazy("index")  # после входа на главную


class UserLogoutView(View):
    """Выход из аккаунта допускает только POST-запросы."""
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _("Вы разлогинены"))
        return redirect("index")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
