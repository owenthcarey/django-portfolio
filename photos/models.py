from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    image = models.ImageField(upload_to="photos/", null=True, blank=True)

    def __str__(self):
        return self.title
