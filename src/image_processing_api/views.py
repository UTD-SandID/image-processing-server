from django.core import serializers

from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from image_processing_api.serializers import ImageSerializer
from utils.tasks import process_image
from image_processing.models import SandImage


class SandImageUploadView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            process_image.apply_async(args=[instance.id]) # Asynchronous task scheduler can't connect
            return Response({'message': 'Image successfully uploaded to server.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SandImageList(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    """
    List all sandImages
    """
    def get(self, request, format=None):
        user = self.request.user
        snippets = SandImage.objects.filter(owner=user)
        serializer = ImageSerializer(snippets, many=True)
        return Response(serializer.data)

