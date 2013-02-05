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
    # url(r'^$', 'app.views.index', name='index'),
    url(r'^register$', 'account.views.register', name='register'),
    url(r'^login$', 'account.views.login', name='login'),
    url(r'^logout$', 'account.views.logout', name='logout'),
    url(r'^deshboard$', 'post.views.deshboard', name='deshboard'),
    url(r'^new$', 'post.views.new_post', name='new_post'),
    # url(r'^settings$', 'account.views.settings', name='settings'),
    # url(r'^taged/(?P<tag_name>[-\w]+)', '', name='tag'),
    # url(r'^blog/(?P<user_slug>[-\w]+), '', name='usr_index'),
    # url(r'^blog/(?P<user_slug>[-\w]+)/taged/(?P<tag_slug>[-\w]+), '',
                                                # name='usr_tag'),
    # url(r'^blog/(?P<user_slug>[-\w]+)/post/(?P<post_id>\d+),
    # 'post.views.detail', name='post_detail'),
    # url(r'^blog/(?P<user_slug>[-\w]+)/post/(?P<post_id>\d+)/(?P<post_slug>[-\w]+),
    # 'post.views.detail', name='post_detail'),
)
