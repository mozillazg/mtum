#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest


def bad_request(view_func=None, redirect=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                if redirect:
                    return HttpResponseRedirect(redirect)
                else:
                    return HttpResponseBadRequest('Bad Request!')
        return _wrapped_view

    if not view_func:
        def foo(view_func):
            return decorator(view_func)
        return foo

    else:
        return decorator(view_func)
