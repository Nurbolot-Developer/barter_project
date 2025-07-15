#!/usr/bin/env python
"""Утилита командной строки Django для административных задач."""
import os
import sys

def main():
    # Устанавливаем переменную окружения для настроек Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barter_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что Django установлен и "
            "доступен в переменной окружения PYTHONPATH. Не забыли активировать виртуальное окружение?"
        ) from exc
    # Выполняем команду, переданную в командной строке
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
