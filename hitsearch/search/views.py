from django.shortcuts import render_to_response
from search.models import *
import HITS
import query

def index(request):
    q = request.GET.get('q')
    s = request.GET.get('s')
    if s == 'h': s == 'hubbiness'
    else: s == 'authority'

    if q:
        results = query.get_results(q, s)
        return render_to_response('search/results.html', { 'q': q, 's': s, 'results': results })
    else:
        return render_to_response('search/index.html', { })
    

