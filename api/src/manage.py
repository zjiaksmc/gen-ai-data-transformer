#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/zjia/Workspace/gen-ai-data-transformer/sa_token.json"
    os.environ["GITHUB_SECRET"] = "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"
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
