#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.template.defaultfilters import slugify
# from unidecode import unidecode


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            # self.slug = slugify(unidecode(self.user.username))
            self.slug = self.user.username
        super(UserProfile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
