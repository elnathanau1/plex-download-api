import json
import sys
from os import path as ospath
import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from clint.textui import progress

import uuid
from resources import redis_service as redis
import concurrent.futures
import time

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
    return id


def get_download(id):
    return redis.get('DOWNLOAD_STATUS_' + id)

def contains_none(*argv):
    for arg in argv:
        if arg is None:
            return True
    return False
