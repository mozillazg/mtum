#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import TextForm
from .forms import PhotoForm
from .forms import VideoForm
from .models import 


@login_required(login_url=reverse_lazy('login'))
def deshboard(request):
    kind = request.GET.get('new')
    if kind in ('text', 'phote', 'quote', 'link', 'chat', 'audio', 'video'):
        if kind == 'text':
            context = {
                'form': TextForm(),
                'user': request.user,
            }
            return render_to_response('post/new.html', context,
                                      context_instance=RequestContext(request)
    else:
        return HttpResponseRedirect(reverse_lazy('deshboard'))


@login_required(login_url=reverse_lazy('login'))
def new_post(request):
    if request.method == 'POST':
        kind = request.POST.get('kind')
        if kind == 'text':
            form = TextForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                tags = form.cleaned_data['tags']
                # if tags
    else:
        return HttpResponseRedirect(reverse_lazy('deshboard'))
