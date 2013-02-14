#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class TextForm(forms.Form):
    attrs_title = {
        'class': 'text_field big wide',
    }
    attrs_content = {
        'class': 'wide post_two',
    }

    title = forms.CharField(required=False,
                            widget=forms.TextInput(attrs=attrs_title))
    content = forms.CharField(widget=forms.Textarea(attrs=attrs_content))
    tags = forms.CharField(required=False)


class PhotoForm(forms.Form):
    attrs_photo = {
        'class': 'text_field wide',
    }
    attrs_content = {
        'class': 'wide post_caption',
    }

    title = forms.CharField(required=False)
    photo = forms.URLField(widget=forms.TextInput(attrs=attrs_photo))
    url = forms.URLField(required=False,
                         widget=forms.TextInput(attrs=attrs_photo))
    content = forms.CharField(required=False,
                              widget=forms.Textarea(attrs=attrs_content))
    tags = forms.CharField(required=False)


class QuoteForm(forms.Form):
    pass


class LinkForm(forms.Form):
    title = forms.CharField(required=False)
    url = forms.URLField()
    content = forms.CharField(widget=forms.Textarea, required=False)
    tags = forms.CharField(required=False)


class ChatForm(forms.Form):
    pass


class AudioForm(forms.Form):
    pass


class VideoForm(forms.Form):
    title = forms.CharField(required=False)
    code = forms.CharField(widget=forms.Textarea)
    content = forms.CharField(widget=forms.Textarea, required=False)
    tags = forms.CharField(required=False)
