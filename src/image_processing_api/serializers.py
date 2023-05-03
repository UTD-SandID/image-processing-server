from rest_framework import serializers
from rest_framework import serializers
from image_processing.models import SandImage

# TODO: Fields need to be changed when proper API is established
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SandImage
        fields = ('image', 'image_uri', 'latitude', 'longitude', 'coin', 'status', 'error')
