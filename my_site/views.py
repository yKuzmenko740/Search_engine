from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.

def home(request):
    return render(request, template_name='base.html')

def new_search(request):
    search = request.POST.get('search')
    print(search)
    request_for_frontend = {
        'search': search,
    }
    return render(request, 'my_site/new_search.html', context=request_for_frontend)
