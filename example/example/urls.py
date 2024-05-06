from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from example import settings
from example.views import index, create_profile_picture, create_cat_picture, login_view

urlpatterns = [
   path('', index, name='index'),
   path('login/', login_view, name='login'),
   path('upload_profile_picture/', create_profile_picture, name='upload_profile_picture'),
   path('upload_cat_picture/', create_cat_picture, name='upload_cat_picture'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)