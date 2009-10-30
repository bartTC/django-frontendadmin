import datetime
from django.db.models import permalink
from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    published = models.DateTimeField(default=datetime.datetime.now)
    public = models.BooleanField(default=True)
        
    class Meta:
        verbose_name = u'Weblog Entry'
        verbose_name_plural = u'Weblog Entries'

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('weblog_details', (str(self.pk),))

