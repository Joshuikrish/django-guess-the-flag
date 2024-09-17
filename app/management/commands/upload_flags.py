import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Flag  # Adjust the import based on your app name

class Command(BaseCommand):
    help = 'Upload flags from a directory and populate the database'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Path to the directory containing flag images')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory']

        if not os.path.exists(directory_path):
            self.stdout.write(self.style.ERROR('Directory does not exist'))
            return

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    country_name = os.path.splitext(file)[0]  # Assuming the file name is the country name
                    with open(file_path, 'rb') as f:
                        flag_image = File(f)
                        flag, created = Flag.objects.get_or_create(name=country_name)
                        flag.image.save(file, flag_image, save=True)
                        self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {file}'))

        self.stdout.write(self.style.SUCCESS('All flags have been uploaded successfully'))