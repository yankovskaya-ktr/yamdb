import csv
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = ('Import data from a CSV file to the database.'
            'Pass a file name as a 1-st argument,'
            'a model name as a 2-nd argument')

    APP_NAMES = [
        'reviews',
        'users',
    ]

    def add_arguments(self, parser):
        parser.add_argument('csv_name')
        parser.add_argument('model_name')

    def get_model_from_apps(self, model_name, app_names):
        model = None
        for app in app_names:
            try:
                model = apps.get_model(app, model_name)
                break
            except LookupError:
                pass
        if not model:
            raise CommandError(f'{model_name} model  does not exist')
        return model

    def handle(self, *args, **options):
        csv_name = options['csv_name']
        model_name = options['model_name']
        file_path = os.path.join(settings.CSV_DIR, csv_name)

        model = self.get_model_from_apps(model_name, self.APP_NAMES)

        try:
            with open(file_path, encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    model.objects.create(**row)

        except FileNotFoundError:
            raise CommandError(f'{file_path} file does not exist')
        except Exception as e:
            raise CommandError(f'Data import failed: {e}')

        self.stdout.write(self.style.SUCCESS('Successfully imported data'
                          f' from {csv_name} to {model.__name__}'))
