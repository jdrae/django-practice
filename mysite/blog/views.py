from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Post

import urllib
import os
from django.http import HttpResponse, Http404
import mimetypes

def download_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    url = post.uploaded_file.url[1:]
    file_url = urllib.parse.unquote(url)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as f:
            quote_file_url = post.get_file_name()
            response = HttpResponse(f.read(), content_type = mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404

class IndexView(generic.ListView):
    template_name='blog/index.html'
    context_object_name='post_list'

    def get_queryset(self):
        return Post.objects.order_by('-id')[:5]


class DetailView(generic.DetailView):
    model = Post
    template_name='blog/detail.html'