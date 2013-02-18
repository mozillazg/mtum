#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from endless_pagination.decorators import page_template

from .forms import TextForm
from .forms import PhotoForm
from .forms import VideoForm
from .helper import create_tags
from post.models import Post
from post.models import Follow
from post.models import Like


@login_required(login_url=reverse_lazy('login'))
@page_template('dashboard/index_page.html')
def dashboard(request, posts_filter=None, template='dashboard/index.html',
              extra_context=None):
    user = request.user
    if posts_filter == 'mine':
        posts = Post.objects.filter(author=user)
    elif posts_filter == 'likes':
        posts = Post.objects.filter(like__author=user)
    elif posts_filter == 'following':
        follows = Follow.objects.filter(follower=user)
        followings = (follow.following for follow in follows)
        posts = Post.objects.filter(author__in=followings)
    else:
        follows = Follow.objects.filter(follower=user)
        followings = (follow.following for follow in follows)
        posts = Post.objects.filter(Q(author=user) | Q(author__in=followings))

    if posts:
        posts = posts.order_by('-created_at')

    context = {
        'user': user,
        'posts': posts,
        'filter': posts_filter,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context,
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


@login_required(login_url=reverse_lazy('login'))
def new_video(request):
    if request.method == 'POST':
        user = request.user
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.cleaned_data['video']
            content = form.cleaned_data['content']
            tags = form.cleaned_data['tags']
            tags = create_tags(tags)
            post = Post.objects.create(author=user, video=video,
                                       content=content, kind='V')
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
            'form': VideoForm(),
            # 'user': request.user,
            'kind': 'video',
            'action_url': reverse_lazy('new_video'),
        }
        return render_to_response('dashboard/new.html', context,
                                  context_instance=RequestContext(request))


@login_required(login_url=reverse_lazy('login'))
def delete_post(request, post_id):
    referer = request.META.get('HTTP_REFERER')
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
    except ObjectDoesNotExist:
        pass
    finally:
        return HttpResponseRedirect(referer or '/')
