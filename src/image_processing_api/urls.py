from .views import SandImageUploadView
from django.urls import path

app_name = 'blog_api'

urlpatterns = [
    path('upload/', SandImageUploadView.as_view(), name='sandimageupload')
]