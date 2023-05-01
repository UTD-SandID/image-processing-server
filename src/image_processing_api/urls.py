from .views import SandImageUploadView, SandImageList
from django.urls import path

app_name = 'image_processing_api'

urlpatterns = [
    path('upload/', SandImageUploadView.as_view(), name='sandimageupload'),
    path('upload/status', SandImageList.as_view(), name='sandimagestatus')
]