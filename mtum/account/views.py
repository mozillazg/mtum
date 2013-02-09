#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .forms import LoginForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email=email,
                                            password=password)
            return HttpResponseRedirect(reverse_lazy('login'))

    else:
        form = RegisterForm()
    return render_to_response('account/register.html', {'form': form},
                              context_instance=RequestContext(request))


def login(request):
    # TODO use email login
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                log_in(request, user)
                return HttpResponseRedirect(reverse_lazy('deshboard'))
    else:
        form = LoginForm()
    return render_to_response('account/login.html', {'form': form},
                              context_instance=RequestContext(request))


def logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse_lazy('index'))


def forgot_password(request):
    return render_to_response('account/forgot_password.html',
                              context_instance=RequestContext(request))


# @login_required(login_url=reverse_lazy('login'))
# def deshboard(request):
    # pass
@login_required(login_url=reverse_lazy('login'))
def settings(request):
    pass
