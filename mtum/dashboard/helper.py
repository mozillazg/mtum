#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Q
from django.template.defaultfilters import slugify

from unidecode import unidecode

from post.models import Tag
from post.models import Post


def create_tags(tags):
    """创建新 tag 并返回相关 tags 的 QuerySet 列表。

    tags：逗号分隔的 tag 字符串（e.g. 'django, python'）
    return：所有 tag 的查询结果集列表
    """
    tags = (tag.strip() for tag in tags.split(',') if tag.strip())
    related_tags = []
    for tag in tags:
        obj, created = Tag.objects.get_or_create(name=tag)
        related_tags += [obj]
    return tuple(related_tags)


# http://sandrotosi.blogspot.com/2011/04/python-group-list-in-sub-lists-of-n.html
def group_iter(iterator, n=2):
    """ Given an iterator, it returns sub-lists made of n items
    (except the last that can have len < n)
    inspired by http://countergram.com/python-group-iterator-list-function"""
    accumulator = []
    for item in iterator:
        accumulator.append(item)
        if len(accumulator) == n:  # tested as fast as separate counter
            yield accumulator
            accumulator = []  # tested faster than accumulator[:] = []
            # and tested as fast as re-using one list object
    if len(accumulator) != 0:
        yield accumulator


def media_wall(keyword=None):
    tag = slugify(unidecode(keyword))
    posts = Post.objects.filter(Q(kind='P') | Q(kind='T'))
    posts = posts.filter(reblog__isnull=True)
    if keyword:
        posts = posts.filter(Q(tags__name__icontains=keyword)
                             | Q(tags__slug__icontains=tag)
                             | Q(content__icontains=keyword)
                             | Q(title__icontains=keyword))

    posts = posts.order_by('-created_at')
    posts_group = group_iter(posts, 3)
    return posts_group
