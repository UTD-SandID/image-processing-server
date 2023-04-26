from celery import shared_task

from image_processing.models import SandImage

from .error_codes import get_error_message
from .firebase_controller import firebase_image_upload
from .rmbg_contour import getRescaleFactor

def process_image_task(sender, instance, **kwargs):
    coin_diameter = instance.coin_diameter
    image_path = str(instance.image.path)
    var, result_path = getRescaleFactor(image_path, coin_diameter)
    if var == 0:
        setattr(instance, 'status', 0)
        setattr(instance, 'image', result_path)
    elif var == 1:
        setattr(instance, 'status', var)
    instance.save()
    #firebase_image_upload(instance.image.url)

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