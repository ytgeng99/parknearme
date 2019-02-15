
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator
from django.core import serializers

from urllib2 import HTTPError
from urllib import quote, urlencode

import argparse
import json
import sys
import urllib
import requests
import math

API_KEY = ''

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
# TOKEN_PATH = '/oauth2/token'
# Defaults for our simple example.
DEFAULT_TERM = 'Park'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 50

def index(request):
    if 'term' not in request.session:
        request.session['term'] = ''
    if 'location' not in request.session:
        request.session['location'] = ''
    return render(request, 'search/index.html')

def query_api(request):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    # if request.method == 'POST':
    term = request.GET['term'] or DEFAULT_TERM
    request.session['term'] = term

    location = request.GET['location'] or DEFAULT_LOCATION
    request.session['location'] = location
    # print ('location is: {}').format(location)
    categories = ''
    response = search(API_KEY, term, location, categories)

    businesses = response.get('businesses')
    
    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    # paginator = Paginator(businesses, 50)
    # page = request.GET.get('page', 1)
    # paginated_businesses = paginator.page(page)
    # print ("search businesses: {}").format(businesses)
    final_businesses = map(roundDis, businesses)
    return render(request, 'search/results.html', {'businesses': final_businesses})
    # else:
    # 	response = search(API_KEY, request.session['term'], request.session['location'], '')
    #     businesses = response.get('businesses')
    #     # businesses.distance = round(businesses.distance / 1600)
    #     if not businesses:
    #         print(u'No businesses for {0} in {1} found.'.format(term, location))
    #         return

    #     paginator = Paginator(businesses, 10)
    #     page = int(request.GET.get('next_page'))
    #     paginated_businesses = paginator.page(page)

    #     return render(request, 'search/results.html', {'businesses': paginated_businesses})
def filter_search(request):
	
	recommend = request.GET.get('recommended')
	distance = request.GET.get('distance')
	# filtered search
	categories = request.GET.getlist('categories')

	if len(categories) == 0:
		# categories = ', '.join(category)
		# print "string of categories is: {}".format(categories)
		categories = ''
	
	response = search(API_KEY, request.session['term'], request.session['location'], categories)
	businesses = response.get('businesses')
	
	# default recommended
	filtered_businesses = businesses
	# highest rating
	if recommend == 'highestRated':
		filtered_businesses = sorted(filtered_businesses, key=lambda k: k['rating'], reverse=True)
        

	# most reviewed	
	elif recommend == 'mostReviewed':
		filtered_businesses = sorted(filtered_businesses, key=lambda k: k['review_count'], reverse=True)
        
	# distance < 5 miles
	if distance == '5':
		# filtered_businesses = list(filter(lambda x : x['distance'] < 5 * 1600, filtered_businesses))
		# or
		filtered_businesses = [x for x in filtered_businesses if x['distance'] < 5 * 1600]
        
	# distance < 20 miles
	elif distance == '10':
		# filtered_businesses = list(filter(lambda x : x['distance'] < 10 * 1600, filtered_businesses))
		# or
		filtered_businesses = [x for x in filtered_businesses if x['distance'] < 10 * 1600]
        
	# distance < 50 miles
	elif distance == '30':
		# filtered_businesses = list(filter(lambda x : x['distance'] < 30 * 1600, filtered_businesses))
		# or
		filtered_businesses = [x for x in filtered_businesses if x['distance'] < 30 * 1600]

        filtered_businesses = map(roundDis, filtered_businesses)
	return render(request, 'search/filter.html', {'businesses': filtered_businesses})

def needs_search(request, term, location):
	categories = ''
	response = search(API_KEY, term, location, categories)
	businesses = response.get('businesses')
        businesses = map(roundDis,businesses)
    
	return render(request, 'search/needs.html', {'businesses': businesses})

def query_business(request, id):
    business = get_business(API_KEY,id)
    return render(request, 'search/business.html', {'business': business})

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

def search(api_key, term, location, categories):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'categories': categories,
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

def roundDis(x):
    x['distance'] = round(x['distance'] / 1600, 2)
    return x
