import requests
from bs4 import BeautifulSoup
import re
from resources.sbplay_scraper import scrape_download_link as sbplay_scrape
import cloudscraper

MAIN_URL = 'https://animekisa.tv/'


def get_movie_download_link(url):
    return get_episode_download_link(url), {}


def generate_episode_json(link):
    url = MAIN_URL + link.get('href')
    ep_num = link.find('div', {'class': 'infoept2'}).text.strip()
    return {
        'url': MAIN_URL + url,
        'ep_num': ep_num
    }


def show(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    episode_list = soup.find('div', {'class': 'infoepbox'})
    links = episode_list.find_all('a')
    episodes = list(map(generate_episode_json, links))

    return_map = {
        'episodes': list(episodes)
    }

    return return_map


def get_episode_download_link(url):
    try:
        r = requests.get(url)
        vidstream_link = re.search(r'var VidStreaming = "(.+)";', r.text).group(1)

        scraper = cloudscraper.create_scraper()
        r = scraper.get(vidstream_link)
        soup = BeautifulSoup(r.text, features='html.parser')

        # search for a server in the list of servers
        link_servers = soup.find_all('li', {'class': 'linkserver'})
        try:
            sbplay_link = next(link for link in link_servers if 'sbplay' in link['data-video'])['data-video']
            return sbplay_scrape(sbplay_link)
        except StopIteration:
            print("sbplay not found for {}".format(url))
            return None

    except Exception as e:
        print("Error getting download link for {}".format(url))
        return None


print(show("https://animekisa.tv/that-time-i-got-reincarnated-as-a-slime"))