"""
    query.py

    Queries the database for Page objets matching a query, gets their HITS values,
    weights by word frequency, and returns a list of all sorted results that
    matched that query.
"""

from search.models import *
import HITS
import utils

def get_results(query, sort_type='authority', beta=0.0):
    """Queries the database for Page objects matching a query, gets their HITS
       values, weights them by word frequency, and returns a list of sorted
       results.
       sort_type can be either authority or hubbiness
       beta is the weight of the HITS results vs. the word frequency
       when beta=0.0 HITS results are alll that matters and word frequency is multiplied by zero
       when beta=1.0 results are based solely on word frequency."""

    terms = query.split()
    terms = [utils.sanitize(term).lower() for term in terms] # strips accents and punctuation
    
    pages = Page.objects.select_related('tag__word_count')

    for term in terms:
        pages = pages.filter(tag__tag=term)

    if pages:
        # links_query is a list of tuple links, where links_query[i] = (source_url, target_url)
        links_query = Link.objects.filter(source__in=pages).values_list('source__url', 'target__url')
        
        # now build the links dict to pass into HITS
        links = dict([(page.url, []) for page in pages])
        for link in links_query:
            links[link[0]].append(link[1])
        #[links[link[0]].append(link[1]) for link in links_query]

        # run HITS
        (authority, hubbiness) = HITS.HITS(links)

        # give a boost based on word frequency
        tags_query = Tag.objects.filter(page__in=pages).values_list('page__url', 'word_count', 'tag')
        
        # creates a dictionary of {page.url: [count of all terms in page, count of all tags in page]
        tags = dict([(page.url, [0, 0]) for page in pages])
        for tag in tags_query:
            if tag[2] in terms: # term
                tags[tag[0]][0] += tag[1] # add to count of search terms in page
            tags[tag[0]][1] += tag[1] # add to count of all tags in page
        
        # assign the pages hubbiness and authority and weights with term frequency   
        for page in pages:
            page.authority = (1 - beta) * authority[page.url] + beta * tags[page.url][0] / float(tags[page.url][1])
            page.hubbiness = (1 - beta) * hubbiness[page.url] + beta * tags[page.url][0] / float(tags[page.url][1])

        # sort the pages
        if sort_type == 'hubbiness':
            sorter = lambda page: (page.hubbiness, page.authority)
        else:
            sorter = lambda page: (page.authority, page.hubbiness)

        # set the results
        results = sorted(pages, key=sorter, reverse=True)
    else:
        results = []

    return results

