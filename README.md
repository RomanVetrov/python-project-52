![Hexlet Check](https://github.com/RomanVetrov/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=RomanVetrov_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=RomanVetrov_python-project-52)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![Django 6](https://img.shields.io/badge/django-6.0-0C4B33?logo=django&logoColor=white)
![django-bootstrap5](https://img.shields.io/badge/django--bootstrap5-enabled-7952B3?logo=bootstrap&logoColor=white)
![uv](https://img.shields.io/badge/deps-uv-000)
![Ruff](https://img.shields.io/badge/lint-ruff-000000?logo=python&logoColor=white)
![Gunicorn](https://img.shields.io/badge/server-gunicorn-499848?logo=gunicorn&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/db-PostgreSQL-336791?logo=postgresql&logoColor=white)
[![Render](https://img.shields.io/badge/render-live-46E3B7)](https://python-project-52-1tyu.onrender.com)

# Task Manager

Учебный таск-менеджер на Django с поддержкой i18n (en/ru), аутентификацией и CRUD для пользователей, статусов, задач и меток.

- Демо: https://python-project-52-1tyu.onrender.com
- Требования: Python 3.12+, [uv](https://github.com/astral-sh/uv)

## Возможности
- Регистрация, вход/выход, редактирование/удаление собственного профиля
- CRUD статусов и меток (удаление запрещено, если используются)
- Задачи с автором, исполнителем, статусом и множеством меток
- Фильтрация задач по статусу, исполнителю, метке и только своим задачам
- Flash-сообщения и валидация доступа (только автор удаляет задачу)
- Локализация интерфейса (en по умолчанию, ru поддерживается)

## Установка и запуск
```bash
# зависимости
uv sync

# миграции + запуск сервера
uv run python manage.py migrate
uv run python manage.py runserver
```

### Переменные окружения
- `DJANGO_SECRET_KEY` — секретный ключ (обязательно в продакшене)
- `DJANGO_DEBUG` — `1` для включения debug
- `DATABASE_URL` — URL базы (например, Postgres для Render); без него используется SQLite

## Скрипты Makefile
- `make install` — установить зависимости
- `make migrate` — применить миграции
- `make collectstatic` — собрать статику
- `make build` — сборка для Render (`build.sh`)
- `make render-start` — старт gunicorn на Render
- `make lint` / `make format` / `make fix` — проверки и автоисправления ruff
- `make check` — запуск линтера

## Тесты
```bash
uv run python manage.py test
```

## Деплой
Проект развёрнут на Render: https://python-project-52-1tyu.onrender.com  
В сборке используется `make build`, в запуске — `make render-start`; зависимости ставятся через uv.
