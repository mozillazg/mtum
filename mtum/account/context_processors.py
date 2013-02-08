#!/usr/bin/env python
# -*- coding: utf-8 -*-


def status(request):  # 只有一个参数（HttpRequeset 对象）
    is_login = False
    user = request.user
    if user.is_authenticated():
        is_login = True
    context = {'is_login': is_login}

    return context  # 返回值必须是个字典
