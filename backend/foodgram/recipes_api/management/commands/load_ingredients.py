import csv

from django.conf import settings
from django.core.management import BaseCommand

from recipes_api.models import Ingredient


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **kwargs):
        current_dir = r'\data\ingredients.csv'
        data_path = settings.BASE_DIR + current_dir
        with open(
            data_path, 'r', encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)

            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader
            )

        self.stdout.write(self.style.SUCCESS('Successfully load data'))
