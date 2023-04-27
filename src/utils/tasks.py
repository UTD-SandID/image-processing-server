from celery import shared_task

from image_processing.models import SandImage

from .error_codes import get_error_message
from .firebase_controller import firebase_image_upload
from .rmbg_contour import getRescaleFactor

@shared_task()
def process_image(instance_pk):
    instance = SandImage.objects.get(pk=instance_pk)
    coin_diameter = instance.coin
    image_path = str(instance.image.path)
    var, result_path = getRescaleFactor(image_path, coin_diameter)
    if var == 0:
        setattr(instance, 'status', 0)
        setattr(instance, 'image', result_path)
    elif var == 1:
        setattr(instance, 'status', var)
    instance.save()
    firebase_image_upload(instance.image.url)
    return coin_diameter

@shared_task()
def batch_upload():
    entries = SandImage.objects.all()
    for entry in entries:
        status = getattr(entry, 'status')
        if status == 0:
            image_path = entry.image.path
            firebase_image_upload(image_path)
        entry.delete()
    return
