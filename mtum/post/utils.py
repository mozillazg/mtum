#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import sample

from django.db.models import Max


def random_queryset(model, number=None, **filters):
    if not number:
        number = 1
    count = model.objects.filter(**filters).annotate(Max('id'))[0].id__max
    rand_ids = sample(xrange(0, count), number)
    queryset = model.objects.filter(**filters).filter(id__in=rand_ids)
    return queryset
