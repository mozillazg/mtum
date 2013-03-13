#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Tag
from .models import Post
from .models import Like
from .models import Follow


def mark_as_featured(modeladmin, request, queryset):
    queryset.update(kind='F')
    mark_as_featured.short_description = 'Mark selected tag as featured'


def mark_as_normal(modeladmin, request, queryset):
    queryset.update(kind='N')
    mark_as_normal.short_description = 'Mark selected tag as normal'


class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'kind', 'reblog', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'kind')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind')
    list_filter = ('kind',)
    actions = (mark_as_featured, mark_as_normal)

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
