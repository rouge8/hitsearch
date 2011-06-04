from django.shortcuts import render_to_response
from search.models import *
import HITS

def index(request):
    q = request.GET.get('q')
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
            
            results = sorted(pages, cmp=lambda x,y: cmp(x.authority, y.authority), reverse=True)

        else:
            results = []
        
        return render_to_response('search/results.html', { 'q': query, 'results': results })
    else:
        return render_to_response('search/index.html', { })
    

