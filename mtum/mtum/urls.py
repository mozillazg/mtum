from django.conf.urls import patterns, include, url
# from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # url(r'^$', TemplateView.as_view(template_name='base.html')),

    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns(
    '',
    url(r'^register$', 'account.views.register', name='register'),
    url(r'^login$', 'account.views.login', name='login'),
    url(r'^logout$', 'account.views.logout', name='logout'),
    url(r'^forgot_password$', 'account.views.forgot_password',
        name='forgot_password')
)

urlpatterns += patterns(
    'dashboard.views',
    url(r'^dashboard$', 'dashboard', name='dashboard'),
    url(r'^new-text$', 'new_post_text', name='new_post_text'),
    url(r'^new-photo$', 'new_post_photo', name='new_post_photo'),
    # url(r'^new-text$', 'post.views.new_post', name='new_post_text'),
    # url(r'^new-text$', 'post.views.new_post', name='new_post_text'),
)

urlpatterns += patterns(
    '',
    # url(r'^$', 'app.views.index', name='index'),

    url(r'^like/(?P<post_id>\d+)$', 'post.views.like', name='like'),
    url(r'^reblog/(?P<post_id>\d+)$', 'post.views.reblog', name='reblog'),
    url(r'^follow/(?P<user_slug>[-\w+]+)$', 'post.views.follow',
        name='follow'),
    url(r'^unfollow/(?P<user_slug>[-\w+]+)$', 'post.views.unfollow',
        name='unfollow'),
    # url(r'^settings$', 'account.views.settings', name='settings'),
    # url(r'^taged/(?P<tag_name>[-\w]+)', '', name='tag'),

    url(r'^blog/(?P<user_slug>[-\w]+)$', 'post.views.user_index',
        name='user_index'),
    url(r'^blog/(?P<user_slug>[-\w]+)/taged/(?P<tag_slug>[-\w]+)$',
        'post.views.user_index', name='user_tag'),

    url(r'^blog/(?P<user_slug>[-\w]+)/search$', 'post.views.user_search',
        name='user_search'),
    url(r'^blog/(?P<user_slug>[-\w]+)/search/(?P<keyword>[ -\+\w]+)$',
        'post.views.user_search_result', name='user_search_result'),

    url(r'^blog/(?P<user_slug>[-\w]+)/post/(?P<post_id>\d+)$',
        'post.views.detail', name='post_detail'),
    url(r'^blog/(?P<user_slug>[-\w]+)/post/(?P<post_id>\d+)/(?P<post_slug>[-\w]+)$',
        'post.views.detail', name='post_detail_slug'),
)
