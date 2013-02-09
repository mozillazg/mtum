#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
                                'placeholder': 'Email',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                  'placeholder': 'Password',}))
    username = forms.CharField(widget=forms.TextInput(attrs={
                                  'placeholder': 'Username',}))


class LoginForm(forms.Form):
    # email = forms.EmailField(widget=forms.TextInput(attrs={
                                # 'placeholder': 'Email',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                  'placeholder': 'Password',}))
    username = forms.CharField(widget=forms.TextInput(attrs={
                                  'placeholder': 'Username',}))


class ForgotPasswordForm(forms.Form):
    attrs = {
        'placeholder': 'Account email address',
        'autofocus': 'autofocus',
    }
    email = forms.EmailField(widget=forms.TextInput(attrs=attrs))
