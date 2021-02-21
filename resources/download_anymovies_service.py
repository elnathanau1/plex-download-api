import requests
from bs4 import BeautifulSoup, SoupStrainer
import json
import re


def get_movie_download_link(url):
    r = requests.get(url)
    links = BeautifulSoup(r.content, features="html.parser", parse_only=SoupStrainer('a'))
    eplay_link = next((link['href'] for link in links if 'eplay' in link['href']), None)

    r = requests.get(eplay_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    source_links = BeautifulSoup(r.content, features="html.parser", parse_only=SoupStrainer('source'))

    download_link = source_links.find('source')['src']
    headers = {
        'referer' : 'https://eplayvid.com/',
        'sec-ch-ua' : '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile' : '?0',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    return (download_link, headers)
