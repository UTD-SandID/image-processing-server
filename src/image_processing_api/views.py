from django.core import serializers

from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.rmbg_contour import getRescaleFactor
from image_processing_api.serializers import ImageSerializer
from utils.tasks import check_status, process_image_task


class SandImageUploadView(APIView):
    authenticaiton_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print(request.data)
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance_data = serializers.serialize()
            #process_image_task.delay(instance_data)
            return Response({'message': 'success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

