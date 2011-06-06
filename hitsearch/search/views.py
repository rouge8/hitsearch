"""
    views.py

    Views of the search application.
"""

from django.shortcuts import render_to_response
from search.models import *
import query

def index(request):
    """Handles requests to the index view. If requests have a q (query) parameter
       this gets the result of the query and renders the results page.
       else it simply renders the index page."""

    q = request.GET.get('q') # the query terms
    s = request.GET.get('s') # sort type: a - authority, h - hubbiness
    b = request.GET.get('b') # beta: weigting between word frequency and authority/hubbiness

    try: # converts b (beta) to a float
        b = float(b)
        if b > 1.0 or b < 0.0: b = 0.7
    except Exception:
        b = .7 # default beta value

    if q: # gets results is there was a query
        results = query.get_results(q, "authority" if s == "a" else "hubbiness", b)
    else:
        results = None
    return render_to_response('search/index.html', { 'q': q, 's': s, 'b': b, 'results': results })