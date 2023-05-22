from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from django.views.decorators.http import require_POST

from .models import Blog, Like


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_likes"] = Like.objects.filter(
            user=self.request.user, blog_id=self.kwargs["pk"]
        ).exists()
        return context


@login_required
@require_POST
def like_blog(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    like, created = Like.objects.get_or_create(user=request.user, blog=blog)

    if not created:
        # The like already existed, so this is an unlike action
        like.delete()

    return redirect("blogs:detail", pk=blog.id)
