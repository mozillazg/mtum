#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User


class SendForm(forms.Form):
    attrs_recipient = {
        'id': 'to',
    }
    attrs_message = {
        'class': 'font_mono-1',
        'id': 'message',
    }

    sender = forms.CharField(required=False)
    recipient = forms.CharField(widget=forms.TextInput(attrs=attrs_recipient))
    message = forms.CharField(widget=forms.Textarea(attrs=attrs_message))
    reply_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def clean_recipient(self):
        data = self.cleaned_data['recipient']
        if not User.objects.filter(username=data).exists():
            raise forms.ValidationError("This user doesn't exists!")

        return data
