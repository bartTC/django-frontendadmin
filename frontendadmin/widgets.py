from django.forms import Textarea
from django.conf import settings
from django.template import Template, Context
from django.utils.simplejson import encoder
from django.utils.hashcompat import sha_constructor
from time import time

class CKEditor(Textarea):
    config = getattr(settings, 'FRONTEND_CKEDITOR_CONFIG', {
    	'extraPlugins': 'uicolor',
        'uiColor': '#E7EFF6',
        
        #'language' : settings.LANGUAGE_CODE, 
    })
             
    def render(self, name, value, attrs=None):
        #return super(CKEditor, self).render(name, value, attrs) + \
        if value is None: value = ''
        nonce = sha_constructor(str(time())).hexdigest()
        return '''<textarea id="%s" name="%s">%s</textarea><script>CKEDITOR.replace('%s', %s);</script>''' % (nonce, name, value, nonce, encoder.JSONEncoder(True).encode(self.config))
