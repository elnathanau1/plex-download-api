import redis

HOST = 'localhost'
PORT = 6379

# used to wont collide with other apps
APP_NAME = 'PLEX_DOWNLOAD_API'

def connect_redis():
    return redis.Redis(host=HOST, port=PORT, decode_responses=True)

def append_app_name(key):
    return APP_NAME + "-" + key

def save(key, value, expire=172800):
    r = connect_redis()
    return r.set(append_app_name(key), value, ex=expire)

def get(key):
    r = connect_redis()
    return r.get(append_app_name(key))

def delete(key):
    r = connect_redis()
    return r.delete(append_app_name(key))
