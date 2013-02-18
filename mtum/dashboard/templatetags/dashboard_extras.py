#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
# from django.db.models import Q

from post.models import Like
from post.models import Post
from post.models import Follow

register = template.Library()


@register.filter
def display_video(url):
    content = '''<embed
    src="%s"
    allowFullScreen="true" quality="high" width="500" height="365"
    align="middle" allowScriptAccess="always"
    type="application/x-shockwave-flash"></embed>''' % url

    return content


@register.filter
def get_notes_numbers(post):
    number = Like.objects.filter(post=post).count()
    number += Post.objects.filter(reblog=post).count()
    return number


@register.filter
def is_liked(user, post):
    return Like.objects.filter(author=user, post=post).exists()


@register.filter
def posts_numbers(user):
    return Post.objects.filter(author=user).count()


@register.filter
def liked_numbers(user):
    return Like.objects.filter(author=user).count()


@register.filter
def following_numbers(user):
    return Follow.objects.filter(follower=user).count()
