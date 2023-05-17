import datetime
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self) -> bool:
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
