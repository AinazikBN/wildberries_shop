from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Выводит Hello, в терминальном окне'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Hello world'))