install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	@PORT=$${PORT:-8000}; uv run gunicorn task_manager.wsgi:application --bind 0.0.0.0:$$PORT

lint:
	uv run ruff check .

format:
	uv run ruff format .

fix:
	uv run ruff check . --fix

check: lint



