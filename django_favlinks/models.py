from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.conf import settings
from pathlib import Path


class Bookmark(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=True)
    screenshot = models.ImageField(
        upload_to="screenshots/",
        blank=True,
        null=True,
    )
    global_click_count = models.IntegerField(default=0)

    tags = TaggableManager(blank=True, help_text="A comma-separated list of tags.")

    def __str__(self):
        return self.title

    def tag_list(self):
        return ", ".join(o.name for o in self.tags.all())


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)


class UserClickCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)
