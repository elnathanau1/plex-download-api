import json
import sys
from os import path as ospath
import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from datetime import datetime

import uuid
from resources import redis_service as redis
from resources import utilities
import concurrent.futures
import time
from models import db, Download, Session

MAX_DOWNLOAD_IDS = 100
MAX_DOWNLOAD_THREADS = 30
executor = concurrent.futures.ThreadPoolExecutor(MAX_DOWNLOAD_THREADS)

current_milli_time = lambda: int(round(time.time() * 1000))

def download_file(id, download_link, download_location, file_name):
    session = Session()
    start_time = datetime.now()
    path = download_location + file_name

    session.query(Download).filter(Download.id == id).update({'status' : 'START_THREAD', 'last_update' : datetime.now()})
    session.commit()

    try:
        # create download_location folder if does not exist
        Path(download_location).mkdir(parents=True, exist_ok=True)

        # download file
        r = requests.get(download_link, stream=True, timeout=60)
        total_bytes = int(r.headers.get('content-length'))
        downloaded_bytes = 0

        with open(path, 'wb') as f:
            # chunk size 0.5 mb
            for chunk in r.iter_content(chunk_size=524288):
                downloaded_bytes += len(chunk)
                f.write(chunk)
                session.query(Download).filter(Download.id == id).update({'status' : 'DOWNLOADING', 'downloaded_bytes' : utilities.humansize(downloaded_bytes), 'total_bytes' : utilities.humansize(total_bytes), 'last_update' : datetime.now()})
                session.commit()

        # if file too small (under 2k), delete it
        if ospath.getsize(path) < 2 * 1024:
            os.remove(path)
            session.query(Download).filter(Download.id == id).update({'status' : 'DELETED', 'downloaded_bytes' : utilities.humansize(downloaded_bytes), 'total_bytes' : utilities.humansize(total_bytes), 'last_update' : datetime.now()})
            session.commit()

        else:
            session.query(Download).filter(Download.id == id).update({'status' : 'COMPLETED', 'downloaded_bytes' : utilities.humansize(downloaded_bytes), 'total_bytes' : utilities.humansize(total_bytes), 'last_update' : datetime.now()})
            session.commit()

    except requests.exceptions.RequestException as e:
        os.remove(path)
        session.query(Download).filter(Download.id == id).update({'status' : 'CRASHED - ' + str(e), 'downloaded_bytes' : '0 MB', 'total_bytes' : '0 MB', 'last_update' : datetime.now()})
        session.commit()

    except Exception as e:
        session.query(Download).filter(Download.id == id).update({'status' : 'CRASHED - ' + str(e), 'downloaded_bytes' : '0 MB', 'total_bytes' : '0 MB', 'last_update' : datetime.now()})
        session.commit()

    finally:
        Session.close()


def start_download(download_link, download_location, file_name):
    # check if file already exists
    if ospath.exists(download_location + file_name):
        return None

    # generate uuid for identification
    id = str(uuid.uuid4())

    session = Session()
    download = Download(id, download_link, download_location + file_name, 'CREATED_THREAD', '0 MB', '0 MB', datetime.now(), datetime.now())
    session.add(download)
    session.commit()
    Session.close()

    executor.submit(download_file, id, download_link, download_location, file_name)
    return id


def get_download(id):
    download = Download.query.filter(Download.id == id).first()
    if download is not None:
        return json.dumps({
            'id' : str(download.id),
            'download_link' : download.download_link,
            'path' : download.path,
            'status' : download.status,
            'downloaded_bytes' : download.downloaded_bytes,
            'total_bytes' : download.total_bytes,
            'start_time' : download.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_update' : download.last_update.strftime("%m/%d/%Y, %H:%M:%S")
        })
    return None


def get_download_ids(status):
    session = Session()
    downloads = map(lambda download : str(download.id), session.query(Download).filter(Download.status == status))
    return list(downloads)


def get_download_ids_in_progress():
    session = Session()
    downloads = map(lambda download : str(download.id), session.query(Download).filter(Download.status != 'COMPLETED'))
    return list(downloads)


def create_download_path(root_folder, show_name, season):
    return root_folder + show_name + '/Season ' + str(season) + '/'


def create_file_name(show_name, season, ep_num):
    return show_name + '_S' + season + '_E' + ep_num + '.mp4'
