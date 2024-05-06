from django.contrib.auth.models import User
from django.db import models
from aws_config import AWSHandler

pub = AWSHandler.get_media_public()
pri = AWSHandler.get_media_private()

print(f"PUBLIC: {pub} \n PRIVATE: {pri}")


class ProfilePictures(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="profile_pictures", storage=AWSHandler.get_media_public())


class CatPictures(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="cat_pictures", storage=AWSHandler.get_media_private())
