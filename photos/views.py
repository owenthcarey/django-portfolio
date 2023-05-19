from django.utils import timezone
from django.views import generic
from .models import Photo


class IndexView(generic.ListView):
    template_name = "photos/index.html"
    context_object_name = "latest_photo_list"

    def get_queryset(self):
        return Photo.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Photo
    template_name = "photos/detail.html"

    def get_queryset(self):
        return Photo.objects.filter(pub_date__lte=timezone.now())
