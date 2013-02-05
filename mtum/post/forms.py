#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class TextForm(forms.Form):
    title = forms.CharField(required=False)
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(required=False)


class PhotoForm(forms.Form):
    url = forms.URLField()
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(required=False)


class QuoteForm(forms.Form):
    pass


class LinkForm(forms.Form):
    title = forms.CharField(required=False)
    url = forms.URLField()
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(required=False)


class ChatForm(forms.Form):
    pass


class AudioForm(forms.Form):
    pass


class VideoForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(required=False)
