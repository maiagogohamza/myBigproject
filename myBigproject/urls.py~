from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myBigproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^maiagogo/', include('maiagogo.urls')),

)

if settings.DEBUG:
	urlpatterns += patterns(
	'django.views.static',
	(r'media/(?P<path>.*)',
	'serve',
	{'document_root': settings.MEDIA_ROOT}), )
