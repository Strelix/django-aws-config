from django.core.files.storage import default_storage
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from aws_config import AWSHandler
from example.models import ProfilePictures, CatPictures


@receiver(post_delete, sender=CatPictures)
def set_profile_picture_to_none(sender, instance: CatPictures, **kwargs):
    # Check if the file exists in the storage
    if instance.image and AWSHandler._get_existing_storage_class("media_private").exists(instance.image.name):
        instance.image.delete(save=False)


@receiver(pre_save, sender=ProfilePictures)
def delete_old_profile_picture(sender, instance: ProfilePictures, **kwargs):
    if not instance.pk:
        return

    try:
        old_profile: ProfilePictures = ProfilePictures.objects.get(pk=instance.pk)
    except ProfilePictures.DoesNotExist:
        return

    if old_profile.image and old_profile.image != instance.image:
        old_profile.image.delete(save=False)
