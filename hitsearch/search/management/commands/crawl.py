from django.core.management.base import BaseCommand, CommandError
from hitsearch.crawler import Crawler
from hitsearch.search.models import *

class Command(BaseCommand):
    args = '<start_site depth>'
    help = 'Crawls the internet!'

    def handle(self, *args, **options):
        start = Page(start_site)
        start.save()
        ## SOMEHOW GET STUFF FROM CRAWLER
        for url that crawler returned:
            page = Page(url)
            link = Link(target, source, text)
            page.save()
            link.save()

#### THIS IS THE GENERAL IDEA ANYWAY....
#### from https://docs.djangoproject.com/en/1.3/howto/custom-management-commands/
            


