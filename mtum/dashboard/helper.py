#!/usr/bin/env python
# -*- coding: utf-8 -*-

from post.models import Tag


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
