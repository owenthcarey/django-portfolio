from django.views import generic
from .models import Blog


class IndexView(generic.ListView):
    template_name = "blogs/index.html"
    context_object_name = "latest_blog_list"

    def get_queryset(self):
        return Blog.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Blog
    template_name = "blogs/detail.html"
