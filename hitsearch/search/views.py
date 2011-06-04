from django.shortcuts import render_to_response
from search.models import *

def index(request):
    return render_to_response('search/index.html', { })
    
def results(request):
    return render_to_response('search/results.html', { })