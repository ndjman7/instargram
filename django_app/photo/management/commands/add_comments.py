from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from photo.models import Photo, PhotoComment
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        photo = Photo.objects.order_by('-created_date').first()
        local_time = timezone.localtime(timezone.now())
        content = 'hey'
        PhotoComment.objects.create(
            photo=photo,
            author=User.objects.first(),
            content=content
        )