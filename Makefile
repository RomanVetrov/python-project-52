# install: ставим зависимости через uv
install:
	uv sync

# migrate: применяем миграции в текущей БД
migrate:
	uv run python manage.py migrate

# collectstatic: собираем статику для продакшена
collectstatic:
	uv run python manage.py collectstatic --noinput

# build: шаг сборки на Render (устанавливает uv, deps, static, миграции)
build:
	./build.sh

# render-start: команда запуска на Render (gunicorn)
render-start:
	@PORT=$${PORT:-8000}; uv run gunicorn task_manager.wsgi:application --bind 0.0.0.0:$$PORT

# lint: проверяем код стилем ruff
lint:
	uv run ruff check .

# format: автоформат роуффом
format:
	uv run ruff format .

# fix: автофикс замечаний роуффа
fix:
	uv run ruff check . --fix

check: lint


