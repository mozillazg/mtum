#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from .models import UserProfile


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
                             'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                               'placeholder': 'Password'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
                               'placeholder': 'Username'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data.get('email', '')
        username = cleaned_data.get('username', '')

        re_username = r'^[a-zA-Z\d][-a-zA-Z\d]*$'

        if User.objects.filter(email=email).exists():
            msg = 'This email address already exists!'
            self._errors['email'] = self.error_class([msg])
            del cleaned_data['email']

        elif not re.match(re_username, username):
            msg = ('Username may only contain alphanumeric characters or'
                   'dashes and cannot begin with a dash')
            self._errors['username'] = self.error_class([msg])
            del cleaned_data['username']

        elif (UserProfile.objects.filter(slug=slugify(username)).exists()
                or User.objects.filter(username=username).exists()):
            msg = 'This username already exists!'
            self._errors['username'] = self.error_class([msg])
            del cleaned_data['username']

        return cleaned_data


class LoginForm(forms.Form):
    # email = forms.EmailField(widget=forms.TextInput(attrs={
                                # 'placeholder': 'Email',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                               'placeholder': 'Password'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
                               'placeholder': 'Username'}))


class ForgotPasswordForm(forms.Form):
    attrs = {
        'placeholder': 'Account email address',
        'autofocus': 'autofocus',
    }
    email = forms.EmailField(widget=forms.TextInput(attrs=attrs))
