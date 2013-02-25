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
    author = models.ForeignKey(User)
    slug = models.SlugField(max_length=300, null=True, blank=True)

    source = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    quote = models.TextField(null=True, blank=True)
    photo = models.URLField(null=True, blank=True)
    video = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    kind = models.CharField(max_length=1, choices=KIND_CHOICES)
    tags = models.ManyToManyField(Tag, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    reblog = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return '%s-%s' % (str(self.id), self.title or '')

    def save(self, *args, **kwargs):
        if (not self.slug) and self.title:
            self.slug = slugify(unidecode(self.title))
        super(Post, self).save(*args, **kwargs)


class Like(models.Model):
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s-%s' % (str(self.post.id), self.post.title or '')


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower')
    following = models.ForeignKey(User, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.follower.username
