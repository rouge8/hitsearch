from search.models import *
import HITS
import utils

def get_results(query, sort_type='authority'):
    terms = query.split()
    terms = [utils.sanitize(term).lower() for term in terms]
    
    pages = Page.objects.select_related('tag__tag') # this may be super fast?

    for term in terms:
        pages = pages.filter(tag__tag=term)

    if pages:
        links = dict([(page.url,[link.target.url for link in page.link_source.all()]) for page in pages])
        (authority, hubbiness) = HITS.HITS(links)

        for page in pages:
            #print page
            #print authority[page.url]
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
