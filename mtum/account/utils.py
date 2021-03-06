#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User


class EmailBackend(object):
    """
    @author: chris http://djangosnippets.org/snippets/1845/
    updated to 1.3 by Łukasz Kidziński

    Authenticate with e-mail.

    Use the  e-mail, and password

    Should work with django 1.3
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    # http://djangosnippets.org/comments/cr/15/2463/#c4508
    def authenticate(self, username=None, password=None):
        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                pass
        else:
            #We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
