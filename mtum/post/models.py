#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from unidecode import unidecode


class Tag(models.Model):
    KIND_CHOICES = (
        ('F', 'featured'),
        ('N', 'normal'),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES, default='N')
    # user = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    KIND_CHOICES = (
        ('T', 'text'),
        ('P', 'photo'),
        ('Q', 'quote'),
        ('L', 'link'),
        ('C', 'chat'),
        ('A', 'audio'),
        ('V', 'video'),
    )
    user = models.ForeignKey(User)
    slug = models.SlugField(max_length=300, null=False, blank=False)

    title = models.CharField(max_length=300, null=False, blank=False)
    link = models.URLField(null=False, blank=False)
    quote = models.TextField(null=False, blank=False)
    photo = models.URLField(null=False, blank=False)
    video = models.CharField(max_length=500, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    kind = models.CharField(max_length=1, choices=KIND_CHOICES)
    tags = models.ManyToManyField(Tag, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (not self.slug) and self.title:
            self.slug = slugify(unidecode(self.title))
        super(Post, self).save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.post.title


class Reblog(models.Model):
    user = models.ForeignKey(User, related_name='user')
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)
    from_blog = models.ForeignKey(User, related_name='from')

    def __unicode__(self):
        return self.post.title
