#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Q

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


# code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples/
def group(lst, n):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]

    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.

    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    return zip(*[lst[i::n] for i in range(n)])


def group_list(lst, n):
    return group(lst, n)


def media_wall(keyword=None):
    posts = Post.objects.filter(Q(kind='P') | Q(kind='T'))
    posts = posts.filter(reblog__isnull=True)
    if keyword:
        posts = posts.filter(Q(tags__name__icontains=keyword)
                             | Q(tags__slug__icontains=keyword)
                             | Q(content__icontains=keyword)
                             | Q(title__icontains=keyword))

    posts = posts.order_by('-created_at')
    posts_group = group_list(posts, 3)
    return posts_group
