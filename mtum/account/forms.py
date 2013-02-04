#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()


class LoginForm(forms.Form):
    # TODO use email login
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
