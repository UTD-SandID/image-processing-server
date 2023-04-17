from django.db import models

class SandImage(models.Model):
    image_id = models.IntegerField()
    user_id = models.IntegerField()
    coin_diameter = models.FloatField()
    image = models.ImageField(max_length=None)
    status = models.CharField(max_length=200)