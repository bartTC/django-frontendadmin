from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from example_project.weblog.models import Entry

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',
        'django.views.generic.list_detail.object_list', {
            'queryset': Entry.objects.order_by('-published'),
            'template_name': 'weblog_overview.html',
        }, name='weblog_index'
    ),

    url(r'^entry-(?P<object_id>[\d]+)/$',
        'django.views.generic.list_detail.object_detail', {
            'queryset': Entry.objects.order_by('-published'),
            'template_name': 'weblog_details.html',
        }, name='weblog_details'
    ),

    (r'^frontendadmin/', include('frontendadmin.urls')),

    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
