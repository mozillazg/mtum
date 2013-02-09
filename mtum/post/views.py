#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from operator import attrgetter
from itertools import chain
from urllib import unquote

from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Q

from .forms import TextForm
from .forms import PhotoForm
# from .forms import VideoForm
from .helper import create_tags
from .models import Post
from .models import Tag
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
    post = Post.objects.get(id=post_id)
    src_post = deepcopy(post)
    tags = src_post.tags.all()

    user = request.user
    post.reblog = src_post
    post.id = None
    post.author = user
    post.created_at = None
    post.save()
    post.tags.add(*tags)

    return HttpResponseRedirect(referer or '/')


@login_required(login_url=reverse_lazy('login'))
def follow(request, user_slug):
    referer = request.META.get('HTTP_REFERER')
    follower = request.user
    following = UserProfile.objects.get(slug=user_slug).user
    Follow.objects.get_or_create(follower=follower, following=following)

    return HttpResponseRedirect(referer or '/')


@login_required(login_url=reverse_lazy('login'))
def unfollow(request, user_slug):
    referer = request.META.get('HTTP_REFERER')
    follower = request.user
    following = UserProfile.objects.get(slug=user_slug).user
    follow = Follow.objects.get(follower=follower, following=following)
    follow.delete()

    return HttpResponseRedirect(referer or '/')


def user_index(request, user_slug, tag_slug=None):
    page_number = request.GET.get('p', 1)
    userprofile = UserProfile.objects.get(slug=user_slug)
    user = blog_author = userprofile.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    if tag_slug:
        posts = posts.filter(tags__slug__iexact=tag_slug)
        tag_name = Tag.objects.get(slug=tag_slug)
    else:
        tag_name = None

    # Pagination
    limit = 3
    paginator = Paginator(posts, limit)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'blog_author': blog_author,
        'tag_name': tag_name,
        'posts': posts,
    }
    return render_to_response('post/index.html', context,
                              context_instance=RequestContext(request))


def user_search(request, user_slug):
    referer = request.META.get('HTTP_REFERER',
                               reverse_lazy('user_index', user_slug))
    keyword = request.GET.get('q')
    if not keyword:
        return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect(reverse_lazy('user_search_result',
                                                 kwargs={
                                                     'user_slug': user_slug,
                                                     'keyword': keyword,
                                                 }))


def user_search_result(request, user_slug, keyword):
    keyword = unquote(keyword)
    if not keyword:
        return HttpResponseRedirect(reverse_lazy('user_index', user_slug))

    userprofile = UserProfile.objects.get(slug=user_slug)
    user = blog_author = userprofile.user
    posts = Post.objects.filter(Q(author=user) & Q(tags__name__iexact=keyword))
    posts = posts.order_by('-created_at')

    context = {
        'blog_author': blog_author,
        'posts': posts,
        'keyword': keyword,
    }
    return render_to_response('post/search.html', context,
                              context_instance=RequestContext(request))


def detail(request, user_slug, post_id, post_slug=None):
    userprofile = UserProfile.objects.get(slug=user_slug)
    blog_author = userprofile.user
    post = Post.objects.get(id=post_id)
    likes = Like.objects.filter(post=post)
    reblogs = Post.objects.filter(reblog=post)
    notes = sorted(chain(likes, reblogs), key=attrgetter('created_at'),
                   reverse=True)

    if post_slug and post_slug != post.slug:
        return HttpResponseNotFound()
    else:
        context = {
            'blog_author': blog_author,
            'post': post,
            'notes': notes,
        }
        return render_to_response('post/detail.html', context,
                                  context_instance=RequestContext(request))
