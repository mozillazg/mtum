#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Tag
from .models import Post
from .models import Like
from .models import Follow

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow)
