from django.shortcuts import render

from photo.models import Photo


def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})
