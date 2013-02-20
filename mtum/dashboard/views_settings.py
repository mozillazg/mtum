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
    if request.method == 'POST':
        return HttpResponseRedirect(reverse_lazy('settings'))
    else:
        initial = {
            'email': user.email,
            'title': user.get_profile().title,
            'description': user.get_profile().description,
        }
        form = AccountForm(initial=initial)

        context = {
            'form': form,
            'action_url': reverse_lazy('settings'),
            'kind': 'account',
        }
        return render_to_response('settings/index.html', context,
                                  context_instance=RequestContext(request))
