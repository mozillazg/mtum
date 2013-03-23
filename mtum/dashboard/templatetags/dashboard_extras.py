#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django import template
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import resolve
from django.template.defaultfilters import slugify

from post.models import Like
from post.models import Post
from post.models import Follow

register = template.Library()


@register.filter
def display_video(url, size='500x365'):
    """Generate video html code
    """
    width, height = size.lower().split('x')

    html = '''<embed src="%s"
    allowFullScreen="true" quality="high" width="%s" height="%s"
    align="middle" allowScriptAccess="always"
    type="application/x-shockwave-flash"></embed>''' % (url, width, height)

    return html


@register.filter
def get_notes_numbers(post):
    """Get notes numbers of post
    """
    number = Like.objects.filter(post=post).count()
    number += Post.objects.filter(reblog=post).count()
    return number


@register.filter
def is_liked(user, post):
    """Does user liked this post
    """
    return Like.objects.filter(author=user, post=post).exists()


@register.filter
def is_following(user, author):
    """Does user following this author
    """
    return Follow.objects.filter(follower=user, following=author).exists()


@register.filter
def posts_numbers(user):
    """Get user's posts numbers
    """
    return Post.objects.filter(author=user).count()


@register.filter
def liked_numbers(user):
    """Get user liked posts numbers
    """
    return Like.objects.filter(author=user).count()


@register.filter
def following_numbers(user):
    """Get following numbers
    """
    return Follow.objects.filter(follower=user).count()


@register.filter
def follower_numbers(user):
    """Get follower numbers
    """
    return Follow.objects.filter(following=user).count()


@register.filter
def get_blog_url(user):
    """Get user blog url
    """
    return reverse_lazy('user_index',
                        kwargs={'user_slug': user.get_profile().slug})


@register.filter
def is_include(nav_name, path):
    """
    """
    nav = reverse_lazy(nav_name)
    path_name = resolve(path).url_name
    dashboard_sub = ['dashboard', 'mine', 'likes', 'following', 'followers',
                     'new_text', 'new_photo', 'new_video', 'edit_post']
    inbox_sub = ['inbox', 'send', 'reply']
    settings_sub = ['settings']

    if path == nav:
        return True
    elif nav_name == 'dashboard' and path_name in dashboard_sub:
        return True
    elif nav_name == 'inbox' and path_name in inbox_sub:
        return True
    elif nav_name == 'settings' and path_name in settings_sub:
        return True


def blog_index(name):
    name = name.group()
    url = reverse_lazy('user_index', kwargs={'user_slug': slugify(name)})
    return '[%s]<%s>' % (name, url)


@register.filter
def at_link(text):
    name_re = re.compile(r'(?m)(?<=@)\w[-\w]*(?=\s|$)')
    text = re.sub(name_re, blog_index, text)
    return text
