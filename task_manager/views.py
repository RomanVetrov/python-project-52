from django.shortcuts import render


def index(request):
    """Главная страница с приветствием и меню."""
    return render(request, "index.html")


# def test_rollbar(request):
#     """Тестовый view для проверки Rollbar"""
#     # Специально вызываю ошибку
#     raise ValueError("Это тестовая ошибка для проверки Rollbar!")
