#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from operator import attrgetter
from itertools import chain
from urllib import unquote

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify

from endless_pagination.decorators import page_template
from unidecode import unidecode

from account.models import UserProfile
from .models import Post
from .models import Tag
from .models import Like
from .models import Follow
from .utils import object_does_not_exist


@object_does_not_exist
@login_required(login_url=reverse_lazy('login'))
def like(request, post_id=None):
    referer = request.META.get('HTTP_REFERER')
    post = Post.objects.get(pk=post_id)
    user = request.user

    if user != post.author:
        Like.objects.get_or_create(author=user, post=post)

    return HttpResponseRedirect(referer or reverse_lazy('dashboard'))


@object_does_not_exist
@login_required(login_url=reverse_lazy('login'))
def unlike(request, post_id=None):
    referer = request.META.get('HTTP_REFERER')
    post = Post.objects.get(pk=post_id)
    user = request.user

    Like.objects.get(author=user, post=post).delete()

    return HttpResponseRedirect(referer or reverse_lazy('dashboard'))


@object_does_not_exist
@login_required(login_url=reverse_lazy('login'))
def reblog(request, post_id=None):
    referer = request.META.get('HTTP_REFERER')
    post = Post.objects.get(pk=post_id)
    user = request.user
    src_post = deepcopy(post)
    tags = src_post.tags.all()

    if user != src_post.author:
        try:
            Post.objects.get(author=user, reblog=src_post)
        except ObjectDoesNotExist:
            post.reblog = src_post
            post.pk = None
            post.author = user
            post.created_at = None
            post.save()
            post.tags = tags

    return HttpResponseRedirect(referer or reverse_lazy('dashboard'))


@object_does_not_exist
@login_required(login_url=reverse_lazy('login'))
def follow(request, user_slug=None):
    referer = request.META.get('HTTP_REFERER')
    follower = request.user
    following = UserProfile.objects.get(slug=user_slug).user
    if follower != following:
        Follow.objects.get_or_create(follower=follower, following=following)

    return HttpResponseRedirect(referer or reverse_lazy('dashboard'))


@object_does_not_exist
@login_required(login_url=reverse_lazy('login'))
def unfollow(request, user_slug):
    referer = request.META.get('HTTP_REFERER')
    follower = request.user
    following = UserProfile.objects.get(slug=user_slug).user
    follow = Follow.objects.get(follower=follower, following=following)
    follow.delete()

    return HttpResponseRedirect(referer or reverse_lazy('dashboard'))


@object_does_not_exist
@page_template('post/index_page.html')
def user_index(request, user_slug, tag_slug=None,
               template='post/index.html', extra_context=None):
    userprofile = UserProfile.objects.get(slug=user_slug)
    user = blog_author = userprofile.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    if tag_slug:
        posts = posts.filter(tags__slug__iexact=tag_slug)
        tag_name = Tag.objects.get(slug=tag_slug)
    else:
        tag_name = None

    context = {
        'blog_author': blog_author,
        'tag_name': tag_name,
        'posts': posts,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def user_search(request, user_slug):
    referer = reverse_lazy('user_index', kwargs={'user_slug': user_slug})
    keyword = request.GET.get('q')
    tag = slugify(unidecode(keyword))
    if not tag:
        return HttpResponseRedirect(referer)
    else:
        return user_search_result(request, user_slug, keyword)


def user_search_result(request, user_slug, keyword):
    keyword = unquote(keyword)
    tag = slugify(unidecode(keyword))
    if not tag:
        return HttpResponseRedirect(reverse_lazy('user_index',
                                                 kwargs={
                                                     'user_slug': user_slug,
                                                 }))

    userprofile = UserProfile.objects.get(slug=user_slug)
    user = blog_author = userprofile.user
    posts = Post.objects.filter(author=user)
    posts = posts.filter(Q(tags__name__icontains=keyword)
                         | Q(tags__slug__icontains=tag)
                         | Q(content__icontains=keyword)
                         | Q(title__icontains=keyword))
    posts = posts.order_by('-created_at')

    context = {
        'blog_author': blog_author,
        'posts': posts,
        'keyword': keyword,
    }
    return render_to_response('post/search.html', context,
                              context_instance=RequestContext(request))


@page_template('post/notes_page.html')
def detail(request, user_slug, post_id, post_slug=None,
           template='post/detail.html', extra_context=None):
    try:
        userprofile = UserProfile.objects.get(slug=user_slug)
        post = Post.objects.get(pk=post_id, author=userprofile.user)
        if post_slug and post_slug != post.slug:
            raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse_lazy('user_index',
                                                 kwargs={
                                                     'user_slug': user_slug
                                                 }))
    likes = Like.objects.filter(post=post)
    reblogs = Post.objects.filter(reblog=post)
    blog_author = userprofile.user
    notes = sorted(chain(likes, reblogs), key=attrgetter('created_at'),
                   reverse=True)

    context = {
        'blog_author': blog_author,
        'post': post,
        'notes': notes,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@object_does_not_exist
def random_post(request, user_slug):
    author = UserProfile.objects.get(slug=user_slug).user
    post_id = Post.objects.filter(author=author).order_by('?')[0].pk

    return HttpResponseRedirect(reverse_lazy('post_detail',
                                             kwargs={
                                                 'user_slug': user_slug,
                                                 'post_id': post_id,
                                             }))
