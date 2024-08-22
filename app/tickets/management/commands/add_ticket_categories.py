import csv
from django.core.management.base import BaseCommand
from ...models import Category

class Command(BaseCommand):
    help = 'Add categories to the Category model from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the CSV file containing categories in the format "name,description" per line'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not file_path:
            self.stdout.write(self.style.ERROR('Please provide the path to the CSV file using --file'))
            return

        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row['name'].strip()
                    description = row['description'].strip()
                    
                    category, created = Category.objects.get_or_create(
                        name=name,
                        defaults={'description': description},
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Added category: {name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Skipped existing category: {name}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
        except KeyError:
            self.stdout.write(self.style.ERROR(f'CSV file must contain "name" and "description" columns'))
