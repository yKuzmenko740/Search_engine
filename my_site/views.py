from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from . import models

BASE_OLX_URL = 'https://www.olx.ua/uk/{list}/q-{item}/?page={page}'
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130",
    "accept": "*/*"}
CITIES = ['kiev', 'dnepr', 'kharkov', 'odessa', 'lvov']


def get_pages_count(URL):
    html = get_html(URL)
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all("span", class_="item fleft")
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    data = html.text
    soup = BeautifulSoup(data, 'html.parser')
    tabs = soup.find_all('tr', 'wrap')

    tabs_res = []

    for tab in tabs:
        tabs_title = tab.find('a', 'marginright5 link linkWithHash detailsLink').text.strip()
        tab_url = tab.find('a').get('href')
        tab_price = tab.find('p', 'price').text.strip()
        tab_date_city = tab.find('td', 'bottom-cell').text.replace('\n', " ").strip()
        if tab.find('img', 'fleft'):
            tab_img_url = tab.find('img', 'fleft').get('src')
        else:
            tab_img_url = "https://748073e22e8db794416a-cc51ef6b37841580002827d4d94d19b6.ssl.cf3.rackcdn.com/not-found.png"

        tabs_res.append((tabs_title, tab_url, tab_price, tab_date_city, tab_img_url))
    return tabs_res


def home(request):
    return render(request, template_name='base.html')


def new_search(request):
    search = request.POST.get('search')
    city = request.POST.get('city')
    models.Search.objects.create(search=search, city=city)
    city = city.lower()
    if city not in CITIES:
        city = 'list'
    final_url = BASE_OLX_URL.format(list=city, item=search.replace(" ", "-"), page=1)
    html = get_html(final_url)
    final_tabs = []
    final_tabs.extend(get_content(html))

    request_for_frontend = {
        'search': search,
        'final_tabs': final_tabs,
    }
    return render(request, 'my_site/new_search.html', context=request_for_frontend)


""" 
    INVALID SCHEMA
    *NOT WORKING*
 """
# def new_search(request):
#     search = request.POST.get('search')
#     city = request.POST.get('city')
#     models.Search.objects.create(search=search, city=city)
#     city = city.lower()
#     if city not in CITIES:
#         city = 'list'
#     final_url = BASE_OLX_URL.format(list=city, item=search.replace(" ", "-"), page=1)
#     html = get_html(final_url)
#     final_tabs = []
#     if html.status_code == 200:
#
#         pages_count = get_pages_count(html.text)
#         for page in range(1, pages_count + 1):
#             print(f'Парсинг страницы: {page} из {pages_count} . . .')
#             final_url = BASE_OLX_URL.format(list=city, item=search.replace(" ", "-"), page=page)
#             html = get_html(final_url)
#             final_tabs.extend(get_content(html))
#     else:
#         print("Error")
#
#
#     request_for_frontend = {
#         'search': search,
#         'final_tabs': final_tabs,
#     }
#     return render(request, 'my_site/new_search.html', context=request_for_frontend)
