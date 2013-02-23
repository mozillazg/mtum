#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse_lazy

from .models import Post


# decorator
def object_does_not_exist(func):
    def returned_wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404()
    return returned_wrapper
