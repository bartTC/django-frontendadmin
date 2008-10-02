from django.conf.urls.defaults import *
from frontendadmin.views import add, change, delete, success, success_delete
from django.views.decorators.cache import never_cache

urlpatterns = patterns('',
    url(r'^add/(?P<app_label>[\w]+)/(?P<model_name>[\w]+)/$',
        never_cache(add),
        name='frontendadmin_add'
    ),

    url(r'^change/(?P<app_label>[\w]+)/(?P<model_name>[\w]+)/(?P<instance_id>[\d]+)/$',
        never_cache(change),
        name='frontendadmin_change'
    ),

    url(r'^delete/(?P<app_label>[\w]+)/(?P<model_name>[\w]+)/(?P<instance_id>[\d]+)/$',
        never_cache(delete),
        name='frontendadmin_delete'
    ),

    url(r'^success/$',
        success,
        name='frontendadmin_success'
    ),

    url(r'^success_delete/$',
        success_delete,
        name='frontendadmin_success_delete'
    ),
)
