#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import AccountForm


@login_required(login_url=reverse_lazy('login'))
def account(request, template_name='settings/index.html'):
    user = request.user
    profile = user.get_profile()
    errors = {}
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            try:
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
                    if User.objects.filter(email=email).exists():
                        errors_msg_email = '<ul><li class="error">'
                        errors_msg_email += 'This e-mail address already'
                        errors_msg_email += ' exists!</li></ul>'
                        errors['email'] = errors_msg_email
                        raise Exception()
                    user.email = email

                if (user.check_password(current_password) and new_password
                        and new_password == cm_new_password):
                    user.set_password(new_password)

                user.save()
                profile.save()

                return HttpResponseRedirect(reverse_lazy('settings'))
            except:
                pass
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
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
