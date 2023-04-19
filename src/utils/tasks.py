from celery import shared_task

from image_processing.models import SandImage

from .error_codes import get_error_message
from .firebase_controller import firebase_image_upload

@shared_task
def check_status():
    entries = SandImage.objects.all()
    for entry in entries:
        status = getattr(entry, 'status')
        if status == 0:
            image_path = entry.image.path
            firebase_image_upload(image_path)
        entry.delete()
    return