import requests
from bs4 import BeautifulSoup
import re


# TODO: REFACTOR THIS
def scrape_download_link(sbplay_embed_link):
    r = requests.get(sbplay_embed_link)
    soup = BeautifulSoup(r.content, features='html.parser')
    download_link_button = soup.find('a', {'href': '#'})
    regex_match = re.match(r'download_video\(\'(\w+)\',\'\w\',\'(.+)\'\)', download_link_button['onclick'])
    id = regex_match.group(1)
    hash = regex_match.group(2)

    attempt_list = [
        (id, 'h', hash),
        (id, 'o', hash),
        (id, 'n', hash),
        (id, 'l', hash)
    ]

    for attempt in attempt_list:
        download_page_link = 'https://sbplay.one/dl?op=download_orig&id={}&mode={}&hash={}'.format(*attempt)
        r = requests.get(download_page_link)
        soup = BeautifulSoup(r.content, features='html.parser')
        span = soup.find('span', {'style': 'background:#f9f9f9;border:1px dotted #bbb;padding:7px;'})

        # occasionally there is security issue, but is just a button press to bypass.
        if span is None:
            hash = soup.find('input', {'name': 'hash'})['value']
            download_page_link = 'https://sbplay.one/dl?op=download_orig&id={}&mode=h&hash={}'.format(id, mode, hash)

            r = requests.get(download_page_link)
            soup = BeautifulSoup(r.content, features='html.parser')
            span = soup.find('span', {'style': 'background:#f9f9f9;border:1px dotted #bbb;padding:7px;'})

        if span is not None:
            return span.find('a')['href']
        
    return None
