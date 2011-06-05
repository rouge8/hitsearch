from search.models import *
import HITS
import utils

def get_results(query, sort_type, beta):
    terms = query.split()
    terms = [utils.sanitize(term).lower() for term in terms]
    
    pages = Page.objects.select_related('tag__word_count')

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

        # give a boost based on word frequency
        tags_query = Tag.objects.filter(page__in=pages).values_list('page__url', 'word_count', 'tag')
        
        tags = dict([(page.url, [0, 0]) for page in pages])
        for tag in tags_query:
            if tag[2] in terms:
                tags[tag[0]][0] += tag[1]
            tags[tag[0]][1] += tag[1]
        
        # assign the pages hubbiness and authority     
        for page in pages:
            page.authority = beta * authority[page.url] + (1 - beta) * tags[page.url][0] / float(tags[page.url][1])
            page.hubbiness = beta * hubbiness[page.url] + (1 - beta) * tags[page.url][0] / float(tags[page.url][1])

        # sort the pages
        if sort_type == 'hubbiness': # hubbiness
            sorter = lambda page: (page.hubbiness, page.authority)
        else:
            sorter = lambda page: (page.authority, page.hubbiness)

        # set the results
        results = sorted(pages, key=sorter, reverse=True)
    else:
        results = []

    return results
