from django import forms
from django.utils.translation import ugettext_lazy as _

class FrontendAdminModelForm(forms.ModelForm):
    pass

class DeleteRequestForm(forms.Form):
    do_delete = forms.BooleanField(
        label=_(u'Yes, delete this object'),
        required=True,
    )
