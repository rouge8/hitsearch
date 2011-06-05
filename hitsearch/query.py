from search.models import *
import HITS
import utils
from collections import defaultdict

def get_results(query, sort_type='authority'):
    terms = query.split()
    terms = [utils.sanitize(term).lower() for term in terms]
    
    pages = Page.objects.select_related() # this may be super fast?

    for term in terms:
        pages = pages.filter(tag__tag=term)

    if pages:
        links_query = Link.objects.filter(source__in=pages).order_by('source').values_list('source__url', 'target__url')

        links = defaultdict(list)
        # links_query is a list of tuple links, where links_query[i] = (source_url, target_url)
        # this beautiful list comprehension works like this:
        # for link in links_query:
        #   links[source_url].append(target_url)
        [links[l[0]].append(l[1]) for l in links_query]

        # this adds any pages that have incoming links but no outgoing links.
        # maybe we shouldn't use a default dict and should just add them the first time around?
        for page in pages:
            if not(page.url in links):
                links[page.url] = []

        (authority, hubbiness) = HITS.HITS(links)

        for page in pages:
            page.authority = authority[page.url]
            page.hubbiness = hubbiness[page.url]

        if sort_type == 'hubbiness':
            sorter = lambda page: (page.hubbiness, page.authority)
        else:
            sorter = lambda page: (page.authority, page.hubbiness)

        results = sorted(pages, key=sorter, reverse=True)
    else:
        results = []

    return results
