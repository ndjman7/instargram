import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from photo.models import Photo, PhotoComment
from member.models import MyUser


@csrf_exempt
def photo_list(request):
    photos = Photo.objects.all()
    data = {
        'photo': [photo.to_dict() for photo in photos],
    }
    return HttpResponse(
        json.dumps(data),
        content_type='application/json'
    )

@csrf_exempt
def photo_add(request):
    data = request.POST
    files = request.FILES

    user_id = data['user_id']
    content = data['content']
    image = files['photo']

    author = MyUser.objects.get(id=user_id)
    photo = Photo.objects.create(
        image=image,
        author=author,
        content=content,
    )
    return HttpResponse(
        json.dumps(photo.to_dict()),
        content_type='application/json'
    )


@csrf_exempt
def comment_add(request, photo_pk):
    data = request.POST
    user_id = data['user_id']
    content = data['content']
    photo_id = photo_pk

    author = MyUser.objects.get(id=user_id)
    photo = MyUser.objects.get(id=photo_id)

    photo_comment = PhotoComment.objects.create(
        photo=photo,
        author=author,
        content=content
    )
    return HttpResponse(
        json.dumps(photo_comment.to_dict()),
        content_type='application/json'
    )