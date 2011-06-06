"""
    crawl.py

    Implements a [django management command](https://docs.djangoproject.com/en/dev/howto/custom-management-commands/)
    so that the crawler can be controlled with manage.py and so that the crawler can write to the database.

    Accessed from the main management command i.e. python manage.py crawl <url> <optional depth>
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from hitsearch.crawler import Crawler
from hitsearch.search.models import *
from datetime import datetime
from counter import Counter

class Command(BaseCommand):
    args = '<start_site depth>'
    help = 'Crawls the internet!'

    # this massively speeds up crawling, as without transaction.commit_manually
    # django commits transactions to the database after every object.save(), of
    # which there are many.
    @transaction.commit_manually
    def handle(self, *args, **options):
        start_site = args[0]
        if len(args) > 1: depth = args[1]
        else: depth = -1

        if depth != -1:
            spider = Crawler(start_site,depth=int(depth), rest=250)
        else:
            spider = Crawler(start_site, rest=250)
        
        for page in spider.crawl(): # database is a list of hitsearch.crawler.Page() objects
            page_object,created = Page.objects.get_or_create(url=page.url)
            # created = True if object created now, = False if it already existed

            page_object.discovery_time = datetime.now()
            page_object.title = page.title
            page_object.save()

            # save word counts from page!
            for word in page.word_counts.keys():
                word_object, created = Tag.objects.get_or_create(page=page_object,
                    tag=word)
                word_object.word_count = page.word_counts[word]
                word_object.save()

            # save links!
            for link in page.links:
                target_object,created = Page.objects.get_or_create(url=link)
                target_object.save()
                link_object,created = Link.objects.get_or_create(target=target_object, source=page_object)  # should make .links return text too
                link_object.save()
                
                # save word counts for links i.e. the text of the link
                # this ensures that any object crawled since we added this will
                # have at least some tags associated with it, otherwise what's
                # the point in crawling?
                word_counts = Counter(page.links[link])
                for word,count in word_counts.iteritems():
                    word_object, created = Tag.objects.get_or_create(page=target_object,
                        tag=word)
                    if created:
                        word_object.word_count = count 
                    else:
                        word_object.word_count += count
                    word_object.save()
                
            transaction.commit() # commits this very large transaction to the database
            print 'page %s saved' %page.url
