import requests
from bs4 import BeautifulSoup
import json
import re
from resources import utilities

def generate_episode_json(link):
    url = link['href']
    ep_num = re.search(r'×(.+?)\Z', link.text.strip())[1]
    return {
            'url' : url,
            'ep_num' : ep_num
        }


def show(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ds_videos = soup.find('div', {'class' : 'dsVideos'})
    links = ds_videos.findAll('a', href=True)
    episodes = list(map(generate_episode_json, links))

    return_map = {
        'episodes' : episodes
    }

    return return_map

def get_episode_download_link(url):
    r = requests.get(url)
    show_page_soup = BeautifulSoup(r.content, 'html.parser')
    token_link = show_page_soup.find('a', {'class' : 'thumb mvi-cover'})['href']

    r = requests.get(token_link)
    show_page_soup = BeautifulSoup(r.content, 'html.parser')
    iframe = show_page_soup.find('iframe')
    iframe_src = iframe['src']

    r = requests.get(iframe_src)

    tc = re.search(r'var tc = \'(.+)\'', r.text)[1]
    x_token = _tsd_tsd_ds(tc)
    token = re.search(r'\"_token\": \"(.+)\"', r.text)[1]

    headers = {
        'x-token' : x_token,
        'content-type' : 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    body = {
        'tokenCode' : tc,
        '_token' : token
    }

    r = requests.post('https://123moviesplayer.com/decoding_v3.php', headers=headers, data = body)
    list = json.loads(r.text)

    r = requests.get(list[0])
    soup = BeautifulSoup(r.content, 'html.parser')
    script_tag = soup.findAll("script")
    for script in script_tag:
        if len(script.contents) == 0:
            continue
        text = script.contents[0]
        if "function(p,a,c,k,e,d)" in text:
            text = text.strip()
            unpacked = eval('utilities.unpack' + text[text.find('}(') + 1:-1])
            reversed_unpacked = unpacked[::-1] # for regex purposes, to search backwards (the mp4 is most important)
            link = re.findall(r'(4pm\..+?)":elif', reversed_unpacked)[0][::-1]
            r = requests.head(link)
            if r.headers['Content-Length'] > 2 * 1024:
                return link
            else:
                return None

def _tsd_tsd_ds(s):
    _51x13o = s
    _53Vxx208 = _51x13o[3:29]
    _391Yx73 = _18x125C(_53Vxx208)
    _1x31B = _W79xW2(_391Yx73)
    return _22kx80(_1x31B) + "29"+"370968"

def _18x125C(s):
    return s

def _W79xW2(r):
    return r[::-1]

def _22kx80(n):
    return n
