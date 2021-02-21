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

    return (download_link, {'referer' : 'https://eplayvid.com/'})
