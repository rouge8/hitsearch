from django.db import models
from datetime import datetime

class Page(models.Model):
    url = models.CharField(max_length=500, unique=True, db_index=True)
    discovery_time=(models.DateTimeField(default=datetime.now()))
    authority = models.FloatField(blank=True, null=True)
    hubbiness = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.url

class Link(models.Model):
    target = models.ForeignKey(Page, related_name='link_target', db_index=True)
    source = models.ForeignKey(Page, related_name='link_source', db_index=True)
    #text = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('target', 'source')

    def __unicode__(self):
        output = unicode(self.source) + ' --> ' + unicode(self.target)
        return output

class Tag(models.Model):
    page = models.ForeignKey(Page)
    term_frequency = models.FloatField()
    tag = models.CharField(max_length=500, db_index=True)

    class Meta:
        unique_together = ('page', 'tag')

    def __unicode__(self):
        return unicode(self.page) + ': ' + unicode(self.tag)
