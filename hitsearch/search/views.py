from django.shortcuts import render_to_response
from search.models import *

def index(request):
    if request.GET.get('q'):
        return render_to_response('search/results.html', { })
    else:
        return render_to_response('search/index.html', { })
    
