import requests
from bs4 import BeautifulSoup
import json
import re

SHOWBOX_URL = 'https://showbox.works/ajax/n123embed.php'

def get_movie_download_link(url):
    r = requests.get(url)
    elid = re.search(r"elid = \"(\w+)\"", r.text).group(1)
    token = re.search(r"var tok    = '(\w+)'", r.text).group(1)

    headers = {
        'x-requested-with' : 'XMLHttpRequest',
        'content-type' : 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    form = {
        'action' : 'getMovieEmb',
        'idEl' : elid,
        'token' : token,
        'nopop' : ''
    }

    r = requests.post(SHOWBOX_URL, data=form, headers=headers)
    source_json = json.loads(r.text)
    for key in source_json.keys():
        embed_html = source_json[key]['embed']
        soup = BeautifulSoup(embed_html, 'html.parser')
        src = soup.find("iframe").get('src')
        try:
            if int(requests.head(src).headers['content-length']) > 5 * 1024:
                return src
        except Exception as e:
            pass
    return None
