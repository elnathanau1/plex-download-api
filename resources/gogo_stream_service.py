import requests
from bs4 import BeautifulSoup
import json

MAIN_URL = 'https://gogo-stream.com'
SEARCH_ENDPOINT = 'https://gogo-stream.com/ajax-search.html'

def search(query):
    # create search call
    queries = {'keyword' : query, 'id' : '-1'}
    headers = {'X-Requested-With' : 'XMLHttpRequest'}
    r = requests.get(SEARCH_ENDPOINT, params=queries, headers=headers)

    # create json object from response body
    response_body = json.loads(r.text)
    html_body = response_body['content']

    # run though html parser
    soup = BeautifulSoup(html_body, 'html.parser')

    # create list of pairs (name, link)
    links = list(map(lambda link : {'name' : link.text, 'url' : MAIN_URL + link['href']}, soup.find_all('a')))

    return_map = {
        'source' : 'gogo-stream',
        'search_endpoint' : SEARCH_ENDPOINT,
        'search_results' : links
    }

    return json.dumps(return_map)

def test(query):
    return "Test: " + query
