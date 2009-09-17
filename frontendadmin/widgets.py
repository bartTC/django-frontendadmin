from django.forms import Textarea
from django.conf import settings
from django.template import Template, Context
from django.utils.simplejson import encoder

class CKEditor(Textarea):
    config = getattr(settings, 'FRONTEND_CKEDITOR_CONFIG', {
    	'extraPlugins': 'uicolor',
        'uiColor': '#E7EFF6',
    })
             
    def render(self, name, value, attrs=None):
        return super(CKEditor, self).render(name, value, attrs) + \
        "<script>CKEDITOR.replace('%s', %s);</script>" % \
    (name, encoder.JSONEncoder(True).encode(self.config))
