#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import urllib

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
# from unidecode import unidecode


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField()
    title = models.CharField(max_length=200, default='Untitled', null=True,
                             blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # self.slug = slugify(unidecode(self.user.username))
            self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def get_avatar(self, size=64, default=None):
        # gravatar_base_url = 'https://secure.gravatar.com/'
        gravatar_base_url = 'http://www.gravatar.com/avatar/'
        email = self.user.email
        default = default or 'mm'
        size = size
        md5email = hashlib.md5(email.lower()).hexdigest()

        gravatar_url = '%s%s?' % (gravatar_base_url, md5email)
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
