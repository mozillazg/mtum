from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    kind = None


class Post(models.Model):
    user = models.OneToOneField(User)
    content = models.TextField()
    # kind = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)
