#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import AccountForm


@login_required(login_url=reverse_lazy('login'))
def account(request):
    user = request.user
    profile = user.get_profile()
    errors = None
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            email = form.cleaned_data['email']
            current_password = form.cleaned_data['c_password']
            new_password = form.cleaned_data['n_password']
            cm_new_password = form.cleaned_data['m_password']

            if title != profile.title:
                profile.title = title
            if description != profile.description:
                profile.description = description
            if email != user.email:
                user.email = email
            if (user.check_password(current_password) and new_password
                    and new_password == cm_new_password):
                user.set_password(new_password)

            user.save()
            profile.save()

            return HttpResponseRedirect(reverse_lazy('settings'))
        else:
            errors = form.errors
    else:
        initial = {
            'email': user.email,
            'title': profile.title,
            'description': profile.description,
        }
        form = AccountForm(initial=initial)

    context = {
        'form': form,
        'action_url': reverse_lazy('settings'),
        'kind': 'account',
        'errors': errors,
    }
    return render_to_response('settings/index.html', context,
                              context_instance=RequestContext(request))
