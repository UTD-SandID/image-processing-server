from celery import shared_task

from image_processing.models import SandImage
from django.utils import timezone

from .error_codes import get_error_message
from .firebase_controller import firebase_image_upload
from .rmbg_contour import getRescaleFactor

'''
@shared_task()
def process_image():
    num_success = 0
    entries = SandImage.objects.filter(status='Pending')
    num_entries = len(entries)
    if num_entries == 0:
        return 'No images pending processing'
    for entry in entries:
        #instance = SandImage.objects.get(pk=instance_pk)
        coin_diameter = getattr(entry, 'coin')
        image_path = str(entry.image.path)
        #var = 'Processed'
        var = getRescaleFactor(image_path, coin_diameter)
        if var == 'Processed':
            num_success += 1
            #entry.image = result_path
            setattr(entry, 'status', var)
        else:
            setattr(entry, 'status', 'Processing Failed')
            setattr(entry, 'error', var)
        entry.save()
    #firebase_image_upload(instance.image.url)
    msg = str(num_success) + '/' + str(num_entries) + ' Pending images processed successfully'
    return msg
'''

@shared_task()
def process_image(instance_pk):
    entry = SandImage.objects.get(pk=instance_pk)
    coin_diameter = entry.coin
    image_path = str(entry.image.path)
    var = getRescaleFactor(image_path, coin_diameter)
    if var == 'Processed':
        setattr(entry, 'status', var)
    else:
        setattr(entry, 'status', 'Processing Failed')
        setattr(entry, 'error', var)
    entry.save()
    return var


@shared_task()
def batch_upload():
    entries = SandImage.objects.filter(status='Processed')
    if len(entries) == 0:
        return 'No Processed images found'
    for entry in entries:
        image_path = entry.image.path
        firebase_image_upload(image_path)
        setattr(entry, 'status', 'Uploaded')
        entry.save()
    msg = str(len(entries)) + ' Processed images Uploaded to Firebase'
    return msg


@shared_task()
def batch_delete():
    entries = SandImage.objects.all()
    for entry in entries:
        if entry.expiration < timezone.now():
            entry.delete()
    return str(len(entries)) + ' deleted from database'
