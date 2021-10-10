import requests
from bs4 import BeautifulSoup
import re
from resources.sbplay_scraper import scrape_download_link as sbplay_scrape

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
        'episodes': list(filter(lambda ep: ep['ep_num'].isnumeric(), episodes))
    }

    return return_map


def get_episode_download_link(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='html.parser')
        select = soup.find("select", {"id": "select-iframe-to-display"})
        options = select.find_all('option')
        vidCDN_link = next(option for option in options if "VidCDN" in option.text)['value']

        r = requests.get(vidCDN_link)
        soup = BeautifulSoup(r.content, features='html.parser')
        # first search to see if animeflix is using basic video tag
        video_tag = soup.find("video")
        if video_tag is not None:
            source = video_tag.find("source")
            if source is not None:
                return source["src"]

        # search for a server in the list of servers
        link_servers = soup.find_all('li', {'class': 'linkserver'})
        try:
            sbplay_link = next(link for link in link_servers if 'sbplay' in link['data-video'])['data-video'].replace(
                'embed-', '')
            return sbplay_scrape(sbplay_link)
        except StopIteration:
            print("sbplay not found for {}".format(url))
            return None

    except Exception as e:
        print("Error getting download link for {}".format(url))
        return None
