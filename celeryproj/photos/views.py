from django.shortcuts import render
from django.views import generic

from feedback.forms import FeedbackForm
from photos.models import Photo


class PhotoView(generic.ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    paginate_by = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        context['form'] = FeedbackForm()
        return context
