from django.db import models

class SandImage(models.Model):
    image = models.ImageField(max_length=None)
    latitude = models.FloatField()
    longitude = models.FloatField()
    coin = models.FloatField()
    status = models.IntegerField(default=0)