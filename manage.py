#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from pathlib import Path


def _inject_venv_site_packages_if_needed():
    try:
        import django  # noqa: F401
        return
    except Exception:
        pass

    base = Path(__file__).resolve().parent
    for venv in (base.parent / ".venv", base / ".venv"):
        for site in venv.glob("lib/python*/site-packages"):
            sp = str(site)
            if sp not in sys.path:
                sys.path.insert(0, sp)



def main():
    """Run administrative tasks."""
    _inject_venv_site_packages_if_needed()
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
