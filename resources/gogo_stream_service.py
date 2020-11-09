import requests
from bs4 import BeautifulSoup
import json
import re

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


def generate_episode_json(entry):
    url = MAIN_URL + entry.find('a')['href']
    ep_text = entry.find('div', {'class' : 'name'}).text.strip()
    match_ep_num = re.match(r'.* Episode (.*)', ep_text)
    ep_num = match_ep_num.group(1)
    return {
            'url' : url,
            'ep_num' : ep_num
        }


def show(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    episode_list = soup.find('ul', {'class' : 'listing items lists'})
    episode_entries = episode_list.find_all('li', {'class' : 'video-block'})
    episodes = list(map(generate_episode_json, episode_entries))

    return_map = {
        'episodes' : episodes
    }

    return json.dumps(return_map)


def get_episode_download_link(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    iframe_link = 'https:' + soup.find('iframe')['src']
    download_link = iframe_link.replace('streaming.php', 'download')

    r = requests.get(download_link)
    soup = BeautifulSoup(r.text, 'html.parser')
    download_divs = soup.find_all('div', {'class' : 'dowload'})
    video_links = list(map(lambda div : (div.find('a')['href'], div.find('a').text.strip()), download_divs))
    return choose_download_link(video_links)


def choose_download_link(download_links):
    quality_order = ['720P', '480P', '1080P', 'HDP', '360P']
    for quality in quality_order:
        found = [link for link, description in download_links if quality in description]
        if len(found) != 0:
            return found[0]
    return None
