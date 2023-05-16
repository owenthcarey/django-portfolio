import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published")
    content = models.TextField()

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
