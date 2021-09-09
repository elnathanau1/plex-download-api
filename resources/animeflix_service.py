import requests
from bs4 import BeautifulSoup
import re

MAIN_URL = 'https://animeflix.ws'

def get_movie_download_link(url):
    return (get_episode_download_link(url), {})

def generate_episode_json(entry):
    url = entry.find('a').get('href')
    ep_num = re.match(r'Episode (.*)', entry.find('span').text).group(1)
    return {
        'url': MAIN_URL + url,
        'ep_num': ep_num
    }


def show(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    episode_list = soup.find('ul', {'class': 'episode'})
    episode_entries = episode_list.find_all('li', {'class': 'epi-me'})
    episodes = list(map(generate_episode_json, episode_entries))

    return_map = {
        'episodes': episodes
    }

    return return_map


def get_episode_download_link(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')
    embed_link = soup.find('iframe').get('src')

    r = requests.get(embed_link)
    soup = BeautifulSoup(r.content, features='html.parser')
    download_link = soup.find('video').find('source').get('src')

    return download_link

