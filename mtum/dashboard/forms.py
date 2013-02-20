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
    attrs_tags = {
        'class': 'text_field',
    }

    title = forms.CharField(required=False,
                            widget=forms.TextInput(attrs=attrs_title))
    content = forms.CharField(widget=forms.Textarea(attrs=attrs_content))
    tags = forms.CharField(required=False,
                           widget=forms.TextInput(attrs=attrs_tags))


class PhotoForm(forms.Form):
    attrs_photo = {
        'class': 'text_field wide',
    }
    attrs_content = {
        'class': 'wide post_caption',
    }
    attrs_tags = {
        'class': 'text_field',
    }

    title = forms.CharField(required=False)
    photo = forms.URLField(widget=forms.TextInput(attrs=attrs_photo))
    url = forms.URLField(required=False,
                         widget=forms.TextInput(attrs=attrs_photo))
    content = forms.CharField(required=False,
                              widget=forms.Textarea(attrs=attrs_content))
    tags = forms.CharField(required=False,
                           widget=forms.TextInput(attrs=attrs_tags))


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
    attrs_video = {
        'class': 'text_field wide',
    }
    attrs_content = {
        'class': 'wide post_caption',
    }
    attrs_tags = {
        'class': 'text_field',
    }

    title = forms.CharField(required=False)
    video = forms.URLField(widget=forms.TextInput(attrs=attrs_video))
    content = forms.CharField(required=False,
                              widget=forms.Textarea(attrs=attrs_content))
    tags = forms.CharField(required=False,
                           widget=forms.TextInput(attrs=attrs_tags))


class AccountForm(forms.Form):
    attrs_input = {
        'class': 'text_field',
    }
    attrs_email = {
        'class': 'text_field',
        'style': 'width: 392px;',
    }

    email = forms.EmailField(widget=forms.TextInput(attrs=attrs_email))
    c_password = forms.CharField(required=False,
                                 widget=forms.PasswordInput(attrs=attrs_input))
    n_password = forms.CharField(required=False,
                                 widget=forms.PasswordInput(attrs=attrs_input))
    m_password = forms.CharField(required=False,
                                 widget=forms.PasswordInput(attrs=attrs_input))
    title = forms.CharField(widget=forms.TextInput(attrs=attrs_input))
    description = forms.CharField(widget=forms.Textarea(attrs=attrs_email))
