from django.db.models.signals import post_save
from image_processing.models import SandImage
from signals import process_image

post_save.connect(process_image, sender=SandImage)
