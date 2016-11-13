from django.db import models
from gram import settings
from member.models import MyUser

__all__ = [
    'Photo',
    'PhotoTag',
    'PhotoLike',
    'PhotoComment',
]


class Photo(models.Model):
    image = models.ImageField(upload_to='photo')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.CharField(max_length=200)
    tags = models.ManyToManyField('PhotoTag', blank=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PhotoLike',
        related_name='photo_set_like_users',
    )

    def to_dict(self):
        ret = {
            'id':self.id,
            'image':self.image.url,
            'author':self.author.id,
            'content':self.content,
        }
        return ret


class PhotoTag(models.Model):
    title = models.CharField(max_length=50)


class PhotoComment(models.Model):
    photo = models.ForeignKey(Photo)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()


class PhotoLike(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(MyUser)
    created_date = models.DateTimeField(auto_now_add=True)
