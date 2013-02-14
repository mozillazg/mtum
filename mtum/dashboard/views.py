#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import attrgetter
from itertools import chain

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from endless_pagination.decorators import page_template

from .forms import TextForm
from .forms import PhotoForm
# from .forms import VideoForm
from .helper import create_tags
from post.models import Post
from post.models import Follow


@login_required(login_url=reverse_lazy('login'))
@page_template('dashboard/index_page.html')
def dashboard(request, template='dashboard/index.html', extra_context=None):
    user = request.user
    follows = Follow.objects.filter(follower=user)
    followings = (follow.following for follow in follows)
    posts = Post.objects.filter(Q(author=user) | Q(author__in=followings))
    posts = posts.order_by('-created_at')

    context = {
        'user': user,
        'posts': posts,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def new_post(request):
    kind = request.GET.get('new')
    if kind in ('text', 'photo', 'quote', 'link', 'chat', 'audio', 'video'):
        if kind == 'text':
            context = {
                'form': TextForm(),
                # 'user': request.user,
                'action': reverse_lazy('new_post_text'),
            }
        elif kind == 'photo':
            context = {
                'form': PhotoForm(),
                # 'user': request.user,
                'action': reverse_lazy('new_post_photo'),
            }

        return render_to_response('dashboard/new.html', context,
                                  context_instance=RequestContext(request))
    else:
        # return HttpResponseRedirect(reverse_lazy('dashboard'))
        return render_to_response('dashboard/index.html',
                                  context_instance=RequestContext(request))


@login_required(login_url=reverse_lazy('login'))
def new_text(request):
    if request.method == 'POST':
        user = request.user
        form = TextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            tags = form.cleaned_data['tags']
            tags = create_tags(tags)
            post = Post.objects.create(author=user, title=title,
                                       content=content, kind='T')
            post.tags.add(*tags)

            user_slug = user.get_profile().slug
            if post.slug:
                redirect_link = reverse_lazy('post_detail_slug',
                                             kwargs={
                                                 'user_slug': user_slug,
                                                 'post_id': post.id,
                                                 'post_slug': post.slug,
                                             })
            else:
                redirect_link = reverse_lazy('post_detail',
                                             kwargs={
                                                 'user_slug': user_slug,
                                                 'post_id': post.id,
                                             })
            return HttpResponseRedirect(redirect_link)
    else:
        context = {
            'form': TextForm(),
            # 'user': request.user,
            'kind': 'text',
            'action_url': reverse_lazy('new_text'),
        }
        # return HttpResponseRedirect(reverse_lazy('deshboard'))
        return render_to_response('dashboard/new.html', context,
                                  context_instance=RequestContext(request))


@login_required(login_url=reverse_lazy('login'))
def new_photo(request):
    if request.method == 'POST':
        user = request.user
        form = PhotoForm(request.POST)
        if form.is_valid():
            photo = form.cleaned_data['photo']
            content = form.cleaned_data['content']
            url = form.cleaned_data['url']
            tags = form.cleaned_data['tags']
            tags = create_tags(tags)
            post = Post.objects.create(author=user, photo=photo, link=url,
                                       content=content, kind='P')
            post.tags.add(*tags)

            user_slug = user.get_profile().slug
            if post.slug:
                redirect_link = reverse_lazy('post_detail_slug',
                                             kwargs={
                                                 'user_slug': user_slug,
                                                 'post_id': post.id,
                                                 'post_slug': post.slug,
                                             })
            else:
                redirect_link = reverse_lazy('post_detail',
                                             kwargs={
                                                 'user_slug': user_slug,
                                                 'post_id': post.id,
                                             })
            return HttpResponseRedirect(redirect_link)
    else:
        context = {
            'form': PhotoForm(),
            # 'user': request.user,
            'kind': 'photo',
            'action_url': reverse_lazy('new_photo'),
        }
        # return HttpResponseRedirect(reverse_lazy('deshboard'))
        return render_to_response('dashboard/new.html', context,
                                  context_instance=RequestContext(request))
