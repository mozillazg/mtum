#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy

from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from .forms import TextForm
from .forms import PhotoForm
# from .forms import VideoForm
from .helper import create_tags
from .models import Post
# from .models import Tag
from .models import Like
from .models import Follow
from account.models import UserProfile


@login_required(login_url=reverse_lazy('login'))
def deshboard(request):
    kind = request.GET.get('new', 'text')
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

        return render_to_response('post/new.html', context,
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse_lazy('deshboard'))


@login_required(login_url=reverse_lazy('login'))
def new_post_text(request):
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
        return HttpResponseRedirect(reverse_lazy('deshboard'))


@login_required(login_url=reverse_lazy('login'))
def new_post_photo(request):
    if request.method == 'POST':
        user = request.user
        form = PhotoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = form.cleaned_data['url']
            content = form.cleaned_data['content']
            tags = form.cleaned_data['tags']
            tags = create_tags(tags)
            post = Post.objects.create(author=user, title=title, photo=url,
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
        return HttpResponseRedirect(reverse_lazy('deshboard'))


def detail(request, user_slug, post_id, post_slug=None):
    userprofile = UserProfile.objects.get(slug=user_slug)
    author = userprofile.user
    post = Post.objects.get(id=post_id)
    if post_slug and post_slug != post.slug:
        return HttpResponseNotFound()
    else:
        context = {
            'author': author,
            'post': post,
        }
        return render_to_response('post/detail.html', context,
                                  context_instance=RequestContext(request))


@login_required(login_url=reverse_lazy('login'))
def like(request, post_id):
    referer = request.META.get('HTTP_REFERER')
    post = Post.objects.get(id=post_id)
    user = request.user
    Like.objects.create(author=user, post=post)

    return HttpResponseRedirect(referer or '/')


@login_required(login_url=reverse_lazy('login'))
def reblog(request, post_id):
    referer = request.META.get('HTTP_REFERER')
    # username = request.GET.get('from')
    # from_blog = User.objects.get(username=username)
    post = Post.objects.get(id=post_id)
    src_post = deepcopy(post)

    user = request.user
    # src_post.author = user
    # del src_post.created_at
    # kwargs = src_post.__dict__.copy()
    # kwargs.pop('id')
    # kwargs.pop('created_at')
    # kwargs.pop('_state')
    # kwargs.pop('_author_cache')
    # kwargs.pop('author_id')
    # kwargs['author'] = user
    # Post.objects.create(reblog=src_post, **kwargs)
    post.reblog = src_post
    post.id = None
    post.author = user
    post.created_at = None
    post.save()

    return HttpResponseRedirect(referer or '/')


@login_required(login_url=reverse_lazy('login'))
def follow(request, user_slug):
    referer = request.META.get('HTTP_REFERER')
    follower = request.user
    following = UserProfile.objects.get(slug=user_slug).user
    Follow.objects.create(follower=follower, following=following)

    return HttpResponseRedirect(referer or '/')


def user_index(request, user_slug, tag_slug=None):
    # page = request.GET.get('p')
    user = UserProfile.objects.get(slug=user_slug).user
    posts = Post.objects.filter(author=user)
    follows = Follow.objects.filter(follower=user)
    if tag_slug:
        posts = posts.filter(tags__slug__iexact=tag_slug)
    context = {
        'posts': posts,
        'follows': follows,
    }

    return render_to_response('post/index.html', context,
                              context_instance=RequestContext(request))
