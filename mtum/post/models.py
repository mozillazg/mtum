from django.db import models
from django.contrib.auth.models import User

from tag.modes import Tag


class Post(models.Model):
    user = models.OneToOneField(User)
    content = models.TextField()
    # kind = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)
