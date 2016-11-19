from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from photo.models import Photo, PhotoComment
from django import forms

from photo.tasks import photo_add_after


def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})


class PhotoList(ListView):
    model = Photo
    paginate_by = 3
    context_object_name = 'photos'


@method_decorator(login_required, name='dispatch')
class PhotoCreate(CreateView):
    model = Photo
    fields = ['author', 'image', 'content']
    success_url = reverse_lazy('photo:photo_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        ret = super(PhotoCreate, self).form_valid(form)
        photo_add_after.delay(self.object.pk)
        return ret


class AddCommentForm(forms.Form):
    content = forms.CharField()


class AddComment(SingleObjectMixin, FormView):
    template_name = 'photo/photo_detail.html'
    form_class = AddCommentForm
    model = Photo

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super(AddComment, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        content = form.cleaned_data['content']
        PhotoComment.objects.create(
            photo=self.object,
            author=self.request.user,
            content=content
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('photo:photo_detail', kwargs={'pk': self.object.pk})


class PhotoDisplay(DetailView):
    model = Photo

    def get_context_data(self, **kwargs):
        context = super(PhotoDisplay, self).get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        return context


class PhotoDetail(DetailView):
    def get(self, request, *args, **kwargs):
        view = PhotoDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AddComment.as_view()
        return view(request, *args, **kwargs)


