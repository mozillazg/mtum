#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponseRedirect


def object_does_not_exist(view_func=None, redirect=None):
    """Decorator for views that catch ObjectDoesNotExist Exception.
    if redirect is None, raise Http404 Exception, otherwise Redirect.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                if redirect:
                    return HttpResponseRedirect(redirect)
                else:
                    raise Http404()
        return _wrapped_view

    if not view_func:
        def foo(view_func):
            return decorator(view_func)
        return foo

    else:
        return decorator(view_func)
