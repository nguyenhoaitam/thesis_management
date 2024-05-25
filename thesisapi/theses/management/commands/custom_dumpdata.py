# import sys
#
# from django.core.management.base import BaseCommand
# from django.core.management import call_command
# import codecs
#
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         output_filename = 'theses_data.json'
#
#         with codecs.open(output_filename, 'w', 'utf-8') as f:
#             original_stdout = sys.stdout
#             sys.stdout = f
#
#             app_name = 'theses'
#
#             from django.apps import apps
#             models = apps.get_app_config(app_name).get_models()
#
#             for model in models:
#                 call_command('dumpdata', model._meta.label, indent=4,
#                              use_natural_foreign_keys=True, use_natural_primary_keys=True)
#
#             sys.stdout = original_stdout

import sys
import json
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps
from io import StringIO

class Command(BaseCommand):
    help = 'Dump data from the database to a JSON file'

    def handle(self, *args, **options):
        output_filename = 'theses_data.json'
        app_name = 'theses'

        models = apps.get_app_config(app_name).get_models()

        all_data = []

        for model in models:
            model_name = model._meta.label
            buffer = StringIO()
            call_command('dumpdata', model_name, indent=4, stdout=buffer)  # Loại bỏ các tùy chọn use_natural_foreign_keys và use_natural_primary_keys
            buffer.seek(0)
            data = json.load(buffer)
            if isinstance(data, list):
                all_data.extend(data)
            else:
                all_data.append(data)

        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Successfully dumped data to {output_filename}'))
