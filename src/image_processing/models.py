from django.db import models

class SandImage(models.Model):
    image = models.ImageField(max_length=None)
    image_uri = models.CharField(max_length=200)
    owner: models.ForeignKey('auth.User', related_name="image_owner", on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    coin = models.FloatField()
    status = models.CharField(max_length=20, default='Pending')
    error = models.CharField(max_length=50, default='None')
    
