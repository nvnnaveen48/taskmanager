from django.core.management.base import BaseCommand
from core.models import Task
from django.utils import timezone
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Delete tasks and media files older than 2 days'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timezone.timedelta(days=2)
        old_tasks = Task.objects.filter(created_at__lt=cutoff)
        count = 0
        for task in old_tasks:
            if task.image:
                image_path = task.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            task.delete()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} tasks and their media files older than 2 days.')) 