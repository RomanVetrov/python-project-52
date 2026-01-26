from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.translation import gettext as _


def index(request):
    """Простейший ответ для проверки работы приложения."""
    return HttpResponse(_("Привет из таск менеджера!"))


# def test_rollbar(request):
#     """Тестовый view для проверки Rollbar"""
#     # Специально вызываю ошибку
#     raise ValueError("Это тестовая ошибка для проверки Rollbar!")
