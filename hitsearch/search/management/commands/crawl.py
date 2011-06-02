from django.core.management.base import BaseCommand, CommandError
from hitsearch.crawler import Crawler
from hitsearch.search.models import *

class Command(BaseCommand):
    args = '<start_site depth>'
    help = 'Crawls the internet!'

    def handle(self, *args, **options):
        start_site = args[0]
        if len(args) > 1: depth = args[1]
        else: depth = None

        spider = Crawler(start_site)
        spider.start()
        
        for page in spider.database: # database is a list of hitsearch.crawler.Page() objects
            page_object,created = Page.objects.get_or_create(url=page.url)
            page_object.save()
            for link in page.links:
                target_object,created = Page.objects.get_or_create(url=link)
                target_object.save()
                link_object,created = Link.objects.get_or_create(target=target_object, source=page_object)  # should make .links return text too
                link_object.save()

#### THIS IS THE GENERAL IDEA ANYWAY....
#### from https://docs.djangoproject.com/en/1.3/howto/custom-management-commands/
            


