from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from image_processing_api.serializers import ImageSerializer

class SandImageUploadView(APIView):
    authenticaiton_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']

            # Run image processing on image here

            return Response({'message': 'Image recieved'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
