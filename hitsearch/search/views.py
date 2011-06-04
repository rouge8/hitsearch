from django.shortcuts import render_to_response
from search.models import *
import HITS

def index(request):
    q = request.GET.get('q')
    query = q
    if q:
        q = q.split(' ')
        
        # get the pages
        pages = Page.objects
        for i in q:
            pages = pages.filter(tag__tag__exact=i.lower())
        
        print "got pages"
        # run hits
        links = dict([(page.url,[link.target.url for link in page.link_source.all()]) for page in pages])
        print "LINKS"
        print links
        (authority, hubbiness) = HITS.HITS(links)
        print "got HITS"

        for page in pages:
            print page
            print authority[page.url]
            page.authority = authority[page.url]
            page.hubbiness = hubbiness[page.url]
        
        # sort results
        results = sorted(pages, cmp=lambda x,y: cmp(x.authority, y.authority), reverse=True)
        print "sorted"
        
        return render_to_response('search/results.html', { 'q': query, 'results': results, "s": links })
    else:
        return render_to_response('search/index.html', { })
    

