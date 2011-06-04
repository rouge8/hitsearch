from django.shortcuts import render_to_response
from search.models import *
import HITS

def index(request):
    q = request.GET.get('q')
    s = request.GET.get('s')
    query = q
    if q:
        q = q.split(' ')
        
        pages = Page.objects
        for i in q:
            pages = pages.filter(tag__tag__exact=i.lower())
        
        if pages:
            links = dict([(page.url,[link.target.url for link in page.link_source.all()]) for page in pages])
            (authority, hubbiness) = HITS.HITS(links)
    
            for page in pages:
                print page
                print authority[page.url]
                page.authority = authority[page.url]
                page.hubbiness = hubbiness[page.url]
            
            print s
            if s == 'h':
                results = sorted(pages, key=lambda page: (page.hubbiness, page.authority), reverse=True)
            else:
                results = sorted(pages, key=lambda page: (page.authority, page.hubbiness), reverse=True)
        else:
            results = []
        
        return render_to_response('search/results.html', { 'q': query, 's': s, 'results': results })
    else:
        return render_to_response('search/index.html', { })
    

