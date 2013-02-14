#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.filter
def display_video(url):
    content = '''<embed
    src="%s"
    allowFullScreen="true" quality="high" width="500" height="365"
    align="middle" allowScriptAccess="always"
    type="application/x-shockwave-flash"></embed>''' % url

    return content
