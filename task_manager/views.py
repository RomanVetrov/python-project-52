from django.http import HttpResponse
from django.utils.translation import gettext as _


def index(request):
    """Простейший ответ для проверки работы приложения."""
    return HttpResponse(_("Привет из таск менеджера!"))
