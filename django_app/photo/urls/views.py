from django.conf.urls import url
from .. import views


urlpatterns = [
    # url(r'^photo_list/$', views.photo_list, name='photo_list'),
    url(r'^photo_list/$', views.PhotoList.as_view(), name='photo_list'),
    url(r'^add/$', views.PhotoCreate.as_view(), name='photo_create'),
    url(r'^detail/(?P<pk>[0-9]+)', views.PhotoDetail.as_view(), name='photo_detail'),
]
