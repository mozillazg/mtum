#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Message
from .form import SendForm
from account.models import UserProfile
from .utils import bad_request


@login_required(login_url=reverse_lazy('login'))
def inbox(request, template_name='message/index.html'):
    all_messages = Message.objects.filter(recipient=request.user)
    all_messages = all_messages.filter(is_denied=False)
    all_messages = all_messages.order_by('-sent_at').order_by('is_read')

    context = {
        'all_messages': all_messages,
    }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


@bad_request  # (redirect=reverse_lazy('inbox'))
@login_required(login_url=reverse_lazy('login'))
def send(request, template_name='message/send.html', extra_context=None):
    if request.method == 'POST':
        form = SendForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipient = form.cleaned_data['recipient']
            message = form.cleaned_data['message']
            reply_id = form.cleaned_data['reply_id']

            recipient = User.objects.get(username=recipient)
            if reply_id:
                reply = Message.objects.get(pk=reply_id, recipient=sender)
                Message.objects.create(sender=sender, recipient=recipient,
                                       message=message, reply=reply)
            else:
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


@bad_request  # redirect=reverse_lazy('inbox'))
@login_required(login_url=reverse_lazy('login'))
def reply(request, sender_slug, recipient_slug, message_id):
    sender = UserProfile.objects.get(slug=sender_slug).user
    recipient = UserProfile.objects.get(slug=recipient_slug).user

    initial = {
        'reply_id': message_id,
        'sender': sender.username,
        'recipient': recipient.username,
    }
    form = SendForm(initial=initial)

    extra_context = {'form': form}
    return send(request, extra_context=extra_context)


@bad_request  # redirect=reverse_lazy('inbox'))
@login_required(login_url=reverse_lazy('login'))
def deny(request, message_id=None, purge=False):
    user = request.user
    if purge:
        messages = Message.objects.filter(recipient=user)
        messages.update(is_denied=True)
    else:
        message = Message.objects.get(pk=message_id, recipient=user)
        message.is_denied = True
        message.save()
    return HttpResponseRedirect(reverse_lazy('inbox'))
