from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from . import models

BASE_OLX_URL = 'https://www.olx.ua/uk/list/q-{}/'


def home(request):
    return render(request, template_name='base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_OLX_URL.format(search.replace(" ", "-"))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, 'html.parser')
    tabs = soup.find_all('tr', 'wrap')

    final_tabs = []
    for tab in tabs:
        tabs_title = tab.find('a', 'marginright5 link linkWithHash detailsLink').text.strip()
        tab_url = tab.find('a').get('href')
        tab_price = tab.find('p', 'price').text.strip()
        tab_date_city = tab.find('td', 'bottom-cell').text.replace('\n', " ").strip()
        if tab.find('img', 'fleft'):
            tab_img_url = tab.find('img', 'fleft').get('src')
        else:
            tab_img_url = "https://748073e22e8db794416a-cc51ef6b37841580002827d4d94d19b6.ssl.cf3.rackcdn.com/not-found.png"

        final_tabs.append((tabs_title, tab_url, tab_price, tab_date_city, tab_img_url))
    request_for_frontend = {
        'search': search,
        'final_tabs': final_tabs,
    }
    return render(request, 'my_site/new_search.html', context=request_for_frontend)
