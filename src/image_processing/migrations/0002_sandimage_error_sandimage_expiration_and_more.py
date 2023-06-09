# Generated by Django 4.2.1 on 2023-05-04 15:23

from django.db import migrations, models
import image_processing.models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sandimage',
            name='error',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AddField(
            model_name='sandimage',
            name='expiration',
            field=models.DateTimeField(default=image_processing.models.expiration),
        ),
        migrations.AlterField(
            model_name='sandimage',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
