#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'sent_at', 'is_read', 'is_denied')
    list_filter = ('is_read', 'is_denied', 'sent_at')
    search_fields = ('message',)

admin.site.register(Message, MessageAdmin)
