from search.models import *
import HITS
import utils

def get_results(query, sort_type='a'): # default sort type is authority
    terms = query.split()
    terms = [utils.sanitize(term).lower() for term in terms]
    
    pages = Page.objects

    for term in terms:
        pages = pages.filter(tag__tag=term)

    if pages:
        # links_query is a list of tuple links, where links_query[i] = (source_url, target_url)
        links_query = Link.objects.filter(source__in=pages).values_list('source__url', 'target__url')
        
        # now build the links dict to pass into HITS
        links = dict([(page.url, []) for page in pages])
        [links[link[0]].append(link[1]) for link in links_query]

        # run HITS
        (authority, hubbiness) = HITS.HITS(links)

        # assign the pages hubbiness and authority
        for page in pages:
            page.authority = authority[page.url]
            page.hubbiness = hubbiness[page.url]

        # sort the pages
        if sort_type == 'h': # hubbiness
            sorter = lambda page: (page.hubbiness, page.authority)
        else:
            sorter = lambda page: (page.authority, page.hubbiness)

        # set the results
        results = sorted(pages, key=sorter, reverse=True)
    else:
        results = []

    return results
