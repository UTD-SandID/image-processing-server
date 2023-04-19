from django.dispatch import receiver
from django.db import models
from django.conf import settings

from image_processing.models import SandImage

from .rmbg_contour import getRescaleFactor
from .firebase_controller import firebase_image_upload

import os
    

@receiver(models.signals.post_delete, sender=SandImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from media folder
    when corresponding `SandImage` object is deleted.
    """
    image_path = instance.image.path

    # Check if the file exists
    if os.path.exists(image_path):
        # Delete the file
        os.remove(image_path)

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
                os.remove(old_instance.image.path)
