from django.db import models

class SandImage(models.Model):
    image_id = models.IntegerField()
    user_id = models.IntegerField()
    coin_type = models.CharField(max_length=20)
    image = models.ImageField(max_length=None)
    #ready = models.BooleanField(default=False)


class CoinTypes(models.Model):
    iso_currency_code = models.CharField(max_length=3)
    coin_name = models.CharField(max_length=10)
    coin_length = models.FloatField()
    coin_error = models.FloatField()