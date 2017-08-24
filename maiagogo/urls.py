from django.conf.urls import patterns, include, url
from maiagogo import views
from django.conf import settings

urlpatterns = patterns('',
   
    url(r'^$', 'maiagogo.views.index', name='index'),
    url(r'^weblog/$', 'maiagogo.views.mentor', name='mentor'),
    url(r'^blog/$', 'maiagogo.views.blog', name='blog'),
    #url(r'^browser/$', 'maiagogo.views.mentor', name='mentor'),
    #url(r'^browser_home/$', 'maiagogo.views.index', name='index'),
    url(r'^category/(?P<category_name_url>\w+)/$', 'maiagogo.views.category', name='category'),
    url(r'^add_category/', 'maiagogo.views.add_category', name='add_category'),
    url(r'^category/(?P<category_name_url>\w+)/add_page/$', 'maiagogo.views.add_page', name='add_page'),
    url(r'^goto/', 'maiagogo.views.track_url', name='track_url'),
    url(r'^like_category/', 'maiagogo.views.like_category', name='like_category'),
    url(r'^post/(?P<pk>\d+)/$', 'maiagogo.views.post_detail', name='post_detail'),
    url(r'^post/new/$', 'maiagogo.views.post_new', name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', 'maiagogo.views.post_edit', name='post_edit'),
    url(r'^contact/$', 'maiagogo.views.contact', name='contact'),
    url(r'^register/$', 'maiagogo.views.register', name='register'),
    url(r'^user_login/$', 'maiagogo.views.user_login', name='user_login'),
    url(r'^post/(?P<pk>\d+)/comment/$',	'maiagogo.views.add_comment_to_post', name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', 'maiagogo.views.comment_approve', name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', 'maiagogo.views.comment_remove', name='comment_remove'),
    #url(r'^user_logout/', 'maiagogo.views.user_logout', name='user_logout'),
    #url(r'^aboutMe/$', 'maiagogo.views.aboutMe', name='aboutMe'),
    #url(r'^sample/$', 'maiagogo.views.sample', name='sample'),
    #url(r'^ramadan/$', 'maiagogo.views.ramadan', name='ramadan'),
    #url(r'^islam/$', 'maiagogo.views.islam', name='islam'),
)

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
	urlpatterns += patterns(
	'django.views.static',
	(r'media/(?P<path>.*)',
	'serve',
	{'document_root': settings.MEDIA_ROOT}), )
