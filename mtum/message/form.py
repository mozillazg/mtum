#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class SendForm(forms.Form):
    attrs_recipient = {
        'id': 'to',
    }
    attrs_message = {
        'class': 'font_mono-1',
        'id': 'message',
    }

    # sender = forms.CharField()
    recipient = forms.CharField(widget=forms.TextInput(attrs=attrs_recipient))
    message = forms.CharField(widget=forms.Textarea(attrs=attrs_message))
