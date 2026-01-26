#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from pathlib import Path


def _ensure_venv_on_path():
    """Добавляет site-packages из локального .venv, если он есть (для CI/compose)."""
    base_dir = Path(__file__).resolve().parent  # .../code
    candidates = [
        base_dir / ".venv",          # .venv рядом с manage.py
        base_dir.parent / ".venv",   # .venv на уровень выше
    ]
    for venv_dir in candidates:
        site_packages = sorted(venv_dir.glob("lib/python*/site-packages"))
        if site_packages:
            sp = str(site_packages[0])
            if sp not in sys.path:
                sys.path.insert(0, sp)
            break


def main():
    """Run administrative tasks."""
    _ensure_venv_on_path()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
