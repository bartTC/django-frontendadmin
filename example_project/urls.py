from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from example_project.weblog.models import Entry

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',
        'django.views.generic.list_detail.object_list', {
            'queryset': Entry.objects.filter(public=True).order_by('-published'),
            'template_name': 'weblog_overview.html',
        }, name='weblog_index'
    ),

    url(r'^entry-(?P<object_id>[\d]+)/$',
        'django.views.generic.list_detail.object_detail', {
            'queryset': Entry.objects.filter(public=True).order_by('-published'),
            'template_name': 'weblog_details.html',
        }, name='weblog_details'
    ),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

'''
This example shows, howto set fields for a specific app_label and/or model_name.
Yes, this is ugly. I try to change this behaviour in future. So expect backwards
incompatible changes.
'''
urlpatterns += patterns('',
    (
        # Override frontendadmin url for specific app_label, mode_name
        r'^frontendadmin/change/(?P<app_label>flatpages)/(?P<model_name>flatpage)/(?P<instance_id>[\d]+)/$',

        # Point it to the view (either add, change or delete)
        'frontendadmin.views.change',

        # Provide extra arguments
        {
            # Fields to include
            'form_fields': ('title', 'content'),

            # And/Or fields to exclude
            #'form_exclude': ('title', 'content'),
        }
    ),
)


'''
This is the default frontendadmin inclusion and a fallback for all frontendadmin
links not overwritten above.
'''
urlpatterns += patterns('',
    (r'^frontendadmin/', include('frontendadmin.urls')),
)
