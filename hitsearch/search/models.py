from django.db import models
from datetime import datetime

class Page(models.Model):
    url = models.CharField(max_length=500, unique=True)
    discovery_time=(models.DateTimeField(default=datetime.now()))
    authority = models.FloatField(blank=True, null=True)
    hubbiness = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.url

class Link(models.Model):
    target = models.ForeignKey(Page, related_name='link_target')
    source = models.ForeignKey(Page, related_name='link_source')
    text = models.TextField()

    class Meta:
        unique_together = ('target', 'source')
        # should text also be here?
        # if so, then it's possible for one source page to have multiple links
        # to a target page but with different text

    def __unicode__(self):
        output = unicode(self.source) + ' --> ' + unicode(self.target)
        return output

class Tag(models.Model):
    page = models.ForeignKey(Page)
    importance = models.FloatField() # should this be word frequency or something else?
    tag = models.CharField(500)
    # should there be a type attribute? i.e. title, meta, content, link, etc.?

    def __unicode__(self):
        return unicode(self.page) + ': ' + unicode(self.tag)
