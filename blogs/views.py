from django.utils import timezone
from django.views import generic
from .models import Blog


class IndexView(generic.ListView):
    template_name = "blogs/index.html"
    context_object_name = "latest_blog_list"

    def get_queryset(self):
        """
        Return the last five published blogs (not including those set to be
        published in the future).
        """
        return Blog.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Blog
    template_name = "blogs/detail.html"

    def get_queryset(self):
        """
        Excludes any blogs that aren't published yet.
        """
        return Blog.objects.filter(pub_date__lte=timezone.now())
