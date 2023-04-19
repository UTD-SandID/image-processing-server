from django.dispatch import receiver
from django.db import models
from django.conf import settings

from image_processing.models import SandImage

from .rmbg_contour import getRescaleFactor
from .firebase_controller import firebase_image_upload

@receiver(models.signals.post_save, sender=SandImage)
def process_image(sender, instance, **kwargs):
    coin_diameter = instance.coin_diameter
    image_path = instance.image.path
    var, result_path = getRescaleFactor(image_path, coin_diameter)
    if var == 0:
        setattr(instance, 'status', 0)
        setattr(instance, 'image', result_path)
    elif var == 1:
        setattr(instance, 'status', var)
    instance.save()
    firebase_image_upload(instance.image.path)
    

@receiver(models.signals.post_delete, sender=SandImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from media folder
    when corresponding `SandImage` object is deleted.
    """
    settings.MEDIA_ROOT.delete(instance.image.name)

@receiver(models.signals.pre_save, sender=SandImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old iamge from media folder
    when corresponding `SandImage` object is updated
    with new file.
    """
    if instance.pk:
        # Retrieve the previous state of the model instance from the database
        old_instance = sender.objects.get(pk=instance.pk)
        # Check if the image field has changed
        if old_instance.image != instance.image:
            # Delete the old image file if it exists
            if old_instance.image:
                settings.MEDIA_ROOT.delete(old_instance.image.name)
