"""
    models.py

    Implements Page, Link, and Tag models for the search application.
"""

from django.db import models
from datetime import datetime

class Page(models.Model):
    """Page has url, discovery_time, title and optional authority and hubbiness
       columns. url must be unique."""

    url = models.CharField(max_length=500, unique=True, db_index=True)
    discovery_time=(models.DateTimeField(default=datetime.now()))
    title = models.CharField(max_length=120)

    # authority and hubbiness would be used if we did not perform query-sensitive
    # HITS
    authority = models.FloatField(blank=True, null=True)
    hubbiness = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.url

class Link(models.Model):
    """Link has target and source foreign keys, both of which are Page objects
       and stored in tables Page.link_target and Page.link_source respectively.
       (target, source) must be unique."""

    target = models.ForeignKey(Page, related_name='link_target', db_index=True)
    source = models.ForeignKey(Page, related_name='link_source', db_index=True)

    class Meta:
        unique_together = ('target', 'source')

    def __unicode__(self):
        output = unicode(self.source) + ' --> ' + unicode(self.target)
        return output

class Tag(models.Model):
    """Tag has a foreign key page which is a Page object, and fields for tag name,
       word_count and term_frequency. term_frequency is not currently used in our
       implementation.
       (page, tag) must be unique."""

    page = models.ForeignKey(Page)
    tag = models.CharField(max_length=500, db_index=True)
    word_count = models.IntegerField(blank=True, null=True)
    term_frequency = models.FloatField(blank=True, null=True) # not actually used

    class Meta:
        unique_together = ('page', 'tag')

    def __unicode__(self):
        return unicode(self.page) + ': ' + unicode(self.tag) + ', ' + unicode(self.word_count)
