import requests
from bs4 import BeautifulSoup
import re


def scrape_download_link(sbplay_embed_link):
    r = requests.get(sbplay_embed_link)
    soup = BeautifulSoup(r.content, features='html.parser')
    download_link_button = soup.find('a', {'href': '#'})
    regex_match = re.match(r'download_video\(\'(\w+)\',\'\w\',\'(.+)\'\)', download_link_button['onclick'])
    id = regex_match.group(1)
    hash = regex_match.group(2)
    # TODO: add safety around if mode=h (high) exists. mode=n is another option
    download_page_link = 'https://sbplay.one/dl?op=download_orig&id={}&mode=h&hash={}'.format(id, hash)

    r = requests.get(download_page_link)
    soup = BeautifulSoup(r.content, features='html.parser')
    span = soup.find('span', {'style': 'background:#f9f9f9;border:1px dotted #bbb;padding:7px;'})
    download_link = span.find('a')['href']
    return download_link
