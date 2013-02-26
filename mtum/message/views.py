#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from .models import Message
from .form import SendForm


@login_required(login_url=reverse_lazy('login'))
def send(request, template_name='message/send.html', extra_context=None):
    if request.method == 'POST':
        form = SendForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipient = form.cleaned_data['recipient']
            message = form.cleaned_data['message']
            recipient = User.objects.get(username=recipient)
            Message.objects.create(sender=sender, recipient=recipient,
                                   message=message)
            return HttpResponseRedirect(reverse_lazy('inbox'))
    else:
        form = SendForm()

    context = {
        'form': form,
        'action_url': reverse_lazy('send'),
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


@login_required(login_url=reverse_lazy('login'))
def inbox(request, template_name='message/index.html'):
    all_messages = Message.objects.filter(recipient=request.user)

    context = {
        'all_messages': all_messages,
    }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
