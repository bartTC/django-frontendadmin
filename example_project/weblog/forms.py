from django import forms
from models import Entry
from django.contrib.admin import widgets                                       


class EntryForm(forms.ModelForm):
    published = forms.CharField(widget=widgets.AdminSplitDateTime())
    
    def clean_published(self):
        """
        Join the split admin format into a single DateTime stamp
        turn "[u'2008-10-04', u'05:28:08']" into 2008-10-04 05:28:08
        """
        return filter(lambda c: not c in "u[],\'", self.cleaned_data['published'])
    
    class Meta:
        model = Entry
