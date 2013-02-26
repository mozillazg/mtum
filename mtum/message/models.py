#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    recipient = models.ForeignKey(User, related_name='recipient')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_denied = models.BooleanField(default=False)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replyto')

    def __unicode__(self):
        return self.sender.username
