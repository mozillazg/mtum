#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.contrib.auth import authenticate
from django.template.defaultfilters import slugify

from .forms import RegisterForm
from .forms import LoginForm
from .models import UserProfile


def register(request, template_name='account/register.html',
             msg=None, extra_context=None):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                if UserProfile.objects.filter(slug=slugify(username)):
                    msg = 'This username already exists!'
                    raise Exception()
                elif User.objects.filter(email=email).exists():
                    msg = 'This email address already exists!'
                    raise Exception()
                else:
                    User.objects.create_user(username, email=email,
                                             password=password)
                    return HttpResponseRedirect(reverse_lazy('login'))
            except:
                form = RegisterForm(initial={'username': username,
                                             'email': email})
                extra_context = {
                    'form': form,
                    'msg': msg,
                }
                request.method = 'GET'
                return register(request, msg=msg, extra_context=extra_context)
        else:
            msg = form.errors.get('email')
            if msg:
                msg = 'Please enter a valid e-mail address!'

    else:
        form = RegisterForm()

    context = {
        'form': form,
        'msg': msg,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def login(request, template_name='account/login.html'):
    # TODO use email login
    next = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                log_in(request, user)
                return HttpResponseRedirect(next or reverse_lazy('dashboard'))
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse_lazy('index'))


def forgot_password(request):
    return render_to_response('account/forgot_password.html',
                              context_instance=RequestContext(request))
