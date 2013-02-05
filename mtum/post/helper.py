#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Tag


def create_tag(tags):
    tags = [tag.strip() for tag in tags.split(',')]
    related_tags = []
    for tag in tags:
        if not Tag.objects.filter(name=tag):
            Tag.objects.create(name=tag)
        related_tags += Tag.objects.filter(name=tag)
    return tuple(related_tags)
