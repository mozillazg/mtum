#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse_lazy
# from django.db.models import Q

from post.models import Like
from post.models import Post
from post.models import Follow

register = template.Library()


@register.filter
def display_video(url, size='500x365'):
    width, height = size.lower().split('x')

    html = '''<embed src="%s"
    allowFullScreen="true" quality="high" width="%s" height="%s"
    align="middle" allowScriptAccess="always"
    type="application/x-shockwave-flash"></embed>''' % (url, width, height)

    return html


@register.filter
def get_notes_numbers(post):
    number = Like.objects.filter(post=post).count()
    number += Post.objects.filter(reblog=post).count()
    return number


@register.filter
def is_liked(user, post):
    return Like.objects.filter(author=user, post=post).exists()


@register.filter
def is_following(user, author):
    return Follow.objects.filter(follower=user, following=author).exists()


@register.filter
def posts_numbers(user):
    return Post.objects.filter(author=user).count()


@register.filter
def liked_numbers(user):
    return Like.objects.filter(author=user).count()


@register.filter
def following_numbers(user):
    return Follow.objects.filter(follower=user).count()


@register.filter
def get_blog_url(user):
    return reverse_lazy('user_index',
                        kwargs={'user_slug': user.get_profile().slug})
