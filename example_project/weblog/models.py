import datetime
from django.db.models import permalink
from django.db import models
from django.contrib import admin

class Entry(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    published = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = u'Weblog Entry'
        verbose_name_plural = u'Weblog Entries'

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('weblog_details', (str(self.pk),))

admin.site.register(Entry)
