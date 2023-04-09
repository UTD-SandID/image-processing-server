from rest_framework import serializers

# TODO: Fields need to be changed when proper API is established
class ImageSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    coin_type = serializers.CharField()
    image = serializers.ImageField(max_length=None, allow_empty_file=False)
