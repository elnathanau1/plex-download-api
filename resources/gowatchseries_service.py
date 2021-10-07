import requests
from bs4 import BeautifulSoup
import re
from resources.sbplay_scraper import scrape_download_link as sbplay_scrape

MAIN_URL = 'https://gowatchseries.online'


def get_movie_download_link(url):
    return (get_episode_download_link(url), {})


def generate_episode_json(entry):
    url = entry.find('a').get('href')
    ep_num = re.match(r'.+Episode (.+?)(?:\Z| |-|:)+', entry.find('a')['title']).group(1)
    return {
        'url': MAIN_URL + url,
        'ep_num': ep_num
    }


def show(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    episode_entries = soup.find_all('li', {'class': 'child_episode'})
    episodes = list(map(generate_episode_json, episode_entries))

    return_map = {
        'episodes': list(filter(lambda ep: ep['ep_num'].isnumeric(), episodes))
    }

    return return_map


def get_episode_download_link(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='html.parser')
        embed_link = 'https:' + soup.find('iframe').get('src')

        r = requests.get(embed_link)
        soup = BeautifulSoup(r.content, features='html.parser')
        link_servers = soup.find_all('li', {'class': 'linkserver'})
        try:
            sbplay_link = next(link for link in link_servers if 'sbplay' in link['data-video'])['data-video'].replace(
                'embed-', '')
            return sbplay_scrape(sbplay_link)
        except StopIteration:
            print("sbplay not found for {}".format(url))
            return None

    except Exception as e:
        print(url)
        return None

