from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class LoginRequiredMessageMixin(AccessMixin):
    message = "Вы не авторизованы! Пожалуйста, выполните вход."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, self.message)

        login_url = self.get_login_url()
        next_url = self.request.get_full_path()
        query = urlencode({"next": next_url})
        return redirect(f"{login_url}?{query}")
