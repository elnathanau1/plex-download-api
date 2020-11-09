import json
import sys
from os import path as ospath
import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests

import uuid
from resources import redis_service as redis
import concurrent.futures
import time

MAX_DOWNLOAD_IDS = 100
MAX_DOWNLOAD_THREADS = 5
executor = concurrent.futures.ThreadPoolExecutor(MAX_DOWNLOAD_THREADS)

current_milli_time = lambda: int(round(time.time() * 1000))

def download_file(id, download_link, download_location, file_name):
    start_time = current_milli_time()
    path = download_location + file_name

    redis.save('DOWNLOAD_STATUS_' + id, json.dumps({
        'download_link' : download_link,
        'path' : path,
        'status' : 'START_THREAD',
        'downloaded_bytes' : 0,
        'total_bytes' : 0,
        'start_time' : start_time,
        'last_update' : current_milli_time()
    }))
    try:
        # create download_location folder if does not exist
        Path(download_location).mkdir(parents=True, exist_ok=True)

        # download file
        r = requests.get(download_link, stream=True)
        total_bytes = int(r.headers.get('content-length'))
        downloaded_bytes = 0

        with open(path, 'wb') as f:
            # chunk size 0.5 mb
            for chunk in r.iter_content(chunk_size=524288):
                downloaded_bytes += len(chunk)
                f.write(chunk)
                redis.save('DOWNLOAD_STATUS_' + id, json.dumps({
                    'download_link' : download_link,
                    'path' : path,
                    'status' : 'DOWNLOADING',
                    'downloaded_bytes' : downloaded_bytes,
                    'total_bytes' : total_bytes,
                    'start_time' : start_time,
                    'last_update' : current_milli_time()
                }))

        # if file too small (under 2k), delete it
        if ospath.getsize(path) < 2 * 1024:
            os.remove(path)
            redis.save('DOWNLOAD_STATUS_' + id, json.dumps({
                'download_link' : download_link,
                'path' : path,
                'status' : 'DELETED',
                'downloaded_bytes' : downloaded_bytes,
                'total_bytes' : total_bytes,
                'start_time' : start_time,
                'last_update' : current_milli_time()
            }))

        else:
            redis.save('DOWNLOAD_STATUS_' + id, json.dumps({
                'download_link' : download_link,
                'path' : path,
                'status' : 'COMPLETED',
                'downloaded_bytes' : downloaded_bytes,
                'total_bytes' : total_bytes,
                'start_time' : start_time,
                'last_update' : current_milli_time()
            }))
    except Exception as e:
        redis.save('DOWNLOAD_STATUS_' + id, json.dumps({
            'download_link' : download_link,
            'path' : path,
            'status' : 'CRASHED - ' + str(e),
            'downloaded_bytes' : 0,
            'total_bytes' : 0,
            'start_time' : start_time,
            'last_update' : current_milli_time()
        }))


def start_download(download_link, download_location, file_name):
    # generate uuid for identification
    id = str(uuid.uuid1())

    # save current status into redis
    current_status = {
        'download_link' : download_link,
        'path' : download_location + file_name,
        'status' : 'CREATED_THREAD',
        'downloaded_bytes' : 0,
        'total_bytes' : 0,
        'start_time' : 0,
        'last_update' : current_milli_time()
    }
    redis.save('DOWNLOAD_STATUS_' + id, json.dumps(current_status))

    executor.submit(download_file, id, download_link, download_location, file_name)
    add_download_id(id)
    return id


def get_download(id):
    return redis.get('DOWNLOAD_STATUS_' + id)


def get_all_download_ids():
    download_ids_json = redis.get('DOWNLOAD_IDS')
    if download_ids_json is None:
        return []
    return json.loads(download_ids_json)


def add_download_id(id):
    download_ids = get_all_download_ids()
    if len(download_ids) >= MAX_DOWNLOAD_IDS:
        download_ids.pop(0)
    download_ids.append(id)
    redis.save('DOWNLOAD_IDS', json.dumps(download_ids))


def create_download_path(root_folder, show_name, season):
    return root_folder + show_name + '/Season ' + season + '/'


def create_file_name(show_name, season, ep_num):
    return show_name + '_S' + season + '_E' + ep_num + '.mp4'
