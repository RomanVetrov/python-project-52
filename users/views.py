from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import SignupForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")  # после регистрации на страницу входа


class OnlySelfMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.pk == self.get_object().pk
        )

    def handle_no_permission(self):
        messages.error(
            self.request, "У вас нет прав для изменения другого пользователя"
        )
        return redirect("users:list")


class UserUpdateView(OnlySelfMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")  # после изменения на список пользователей

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно изменён")
        return super().form_valid(form)


class UserDeleteView(OnlySelfMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно удалён")
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы залогинены")
        return response

    def get_success_url(self):
        return reverse_lazy("index")  # после входа на главную


class UserLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "Вы разлогинены")
        return redirect("index")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
