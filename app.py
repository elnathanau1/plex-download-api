from flask import Flask, request
from resources.gogo_stream_service import search as gogo_stream_search
from resources.gogo_stream_service import test as test_search
app = Flask(__name__)

DEFAULT_SOURCE = 'GOGO-STREAM'
SUPPORTED_SOURCES = [
    'GOGO-STREAM',
    'TEST'
]
SEARCH_FUNCTION_MAP = {
    'GOGO-STREAM' : gogo_stream_search,
    'TEST' : test_search
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
