from flask import Flask, request
from resources.gogo_stream_service import search as gogo_stream_search
from resources.gogo_stream_service import get_episode_download_link as gogo_stream_get_episode_download_link
from resources.gogo_stream_service import show as gogo_stream_show

from resources.download_service import start_download, get_download, get_all_download_ids, create_download_path, create_file_name
from resources.utilities import contains_none
import json

app = Flask(__name__)

DEFAULT_SOURCE = 'GOGO-STREAM'
SUPPORTED_SOURCES = [
    'GOGO-STREAM'
]

SEARCH_FUNCTION_MAP = {
    'GOGO-STREAM' : gogo_stream_search
}

SHOW_FUNCTION_MAP = {
    'GOGO-STREAM' : gogo_stream_show
}

GET_EPISODE_DOWNLOAD_LINK_FUNCTION_MAP = {
    'GOGO-STREAM' : gogo_stream_get_episode_download_link
}


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/search")
def search():
    # get query
    query = request.args.get('query')
    if query is None:
        query = ''
    # set api_source from header
    api_source = get_api_source()

    return SEARCH_FUNCTION_MAP[api_source](query)


@app.route("/show")
def show():
    # get show_url from query params
    show_url = request.args.get('show_url')
    if show_url is None:
        return "show_url must be in query parameters", 400
    # set api_source from header
    api_source = get_api_source()

    return SHOW_FUNCTION_MAP[api_source](show_url)


@app.route("/download/episode", methods=['POST'])
def download_episode():
    episode_url = request.json.get('episode_url')
    show_name = request.json.get('show_name')
    season = request.json.get('season')
    ep_num = request.json.get('episode_num')
    root_folder = request.json.get('root_folder')

    if contains_none(episode_url, show_name, season, ep_num, root_folder):
        return "episode_url, show_name, season, ep_num, and root_folder must be included in query params", 400

    # set api_source from header
    api_source = get_api_source()

    download_link = GET_EPISODE_DOWNLOAD_LINK_FUNCTION_MAP[api_source](episode_url)
    download_location = create_download_path(root_folder, show_name, season)
    file_name = create_file_name(show_name, season, ep_num)

    id = start_download(download_link, download_location, file_name)

    return json.dumps({
        'id' : id
    })



@app.route("/download/url", methods=['POST'])
def download_url():
    download_link = request.json.get('download_link')
    download_location = request.json.get('download_location')
    file_name = request.json.get('file_name')

    if contains_none(download_link, download_location, file_name):
        return "download_link, download_location, and file_name must be included in query params", 400

    id = start_download(download_link, download_location, file_name)

    return json.dumps({
        'id' : id
    })


@app.route("/download/status")
def download_status():
    id = request.args.get('id')
    if id is None:
        return "id must be in query parameters", 400

    status = get_download(id)
    if status is None:
        return "could not find status of id: " + id, 400
    return status


@app.route("/download/status/all")
def download_status_all():
    return json.dumps({
            'download_ids' : get_all_download_ids()
        })


def get_api_source():
    # check for X-API-SOURCE header
    api_source = DEFAULT_SOURCE
    if 'X-API-SOURCE' in request.headers:
        new_api_source = request.headers['X-API-SOURCE'].upper()
        if new_api_source in SUPPORTED_SOURCES:
            api_source = new_api_source

    return api_source


if __name__ == '__main__':
    app.run(host="localhost", port=9050, debug=True)
