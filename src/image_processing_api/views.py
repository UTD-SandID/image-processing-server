from django.core import serializers

from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.rmbg_contour import getRescaleFactor
from image_processing_api.serializers import ImageSerializer
from utils.tasks import check_status, process_image


class SandImageUploadView(APIView):
    authenticaiton_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance_data = serializer.serialize(instance)
            process_image.delay(instance_data)
            #var = process_image_task(instance_data)
            return Response({'message': 'success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SandImageStatus(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        print(request.data)

