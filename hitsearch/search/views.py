from django.shortcuts import render_to_response
from search.models import *
import query

def index(request):
    q = request.GET.get('q') # the query terms
    s = request.GET.get('s') # sort type: a - authority, h - hubbiness
    b = request.GET.get('b') # beta: weigting between word frequency and authority/hubbiness

    try:
        b = float(b)
        if b > 1.0 or b < 0.0: b = 0.7
    except Exception:
        b = .7

    if q:
        results = query.get_results(q, "authority" if s == "a" else "hubbiness", b)
        return render_to_response('search/results.html', { 'q': q, 's': s, 'b': b, 'results': results })
    else:
        return render_to_response('search/index.html', { })
