#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Tag
from .models import Post
from .models import Like
from .models import Follow


class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')
    list_filter = ('author',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    list_filter = ('follower', 'following')


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'kind', 'reblog', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
