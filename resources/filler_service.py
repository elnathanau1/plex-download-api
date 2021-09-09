import requests
from bs4 import BeautifulSoup


def is_filler(row):
    return 'filler' in row['class']


def ep_num(row):
    return row.find('td', {'class': 'Number'}).text


def get_filler_eps(filler_list_url):
    try:
        r = requests.get(filler_list_url)
        soup = BeautifulSoup(r.content, features='html.parser')
        rows = soup.find('tbody').find_all('tr')
        filler_rows = filter(is_filler, rows)
        return list(map(ep_num, filler_rows))
    except:
        return []
