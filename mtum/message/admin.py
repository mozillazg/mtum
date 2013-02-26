#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at', 'sender', 'recipient')
    search_fields = ('message',)

admin.site.register(Message, MessageAdmin)
