from django import template

register = template.Library()


@register.filter
def get_avatar(user, size, default=None):
    if not default:
        if size == 128:
            default = 'http://tumblr.3sd.me/static/img/default_avatar_128.gif'
        elif size == 64:
            default = 'http://tumblr.3sd.me/static/img/default_avatar_64.gif'
        elif size == 30:
            default = 'http://tumblr.3sd.me/static/img/default_avatar_30.gif'
        elif size == 40:
            default = 'http://tumblr.3sd.me/static/img/default_avatar_40.gif'
        elif size == 16:
            default = 'http://tumblr.3sd.me/static/img/default_avatar_16.gif'

    avatar_url = user.get_profile().get_avatar(size, default)
    return avatar_url
