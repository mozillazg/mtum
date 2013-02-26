#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse_lazy

from message.models import Message

register = template.Library()


@register.filter
def get_messags_count(user):
    return Message.objects.filter(recipient=user, is_denied=False).count()


@register.filter
def make_as_read(message):
    message.is_read = True
    message.save()
    return message
