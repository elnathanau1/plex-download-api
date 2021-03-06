# plex-download-api
API written to download media from the web for Plex server

## Alembic set up
https://blog.theodo.com/2017/03/developping-a-flask-web-app-with-a-postresql-database-making-all-the-possible-errors/

- `python manage.py db init`
- `python manage.py db migrate`
- `python manage.py db upgrade`


## API Spec
### Search
`GET /search` - Hits search endpoint of api source.

Query params:
- `query`: String

Example response body:
```
{
  "source": "gogo-stream",
  "search_endpoint": "https://gogo-stream.com/ajax-search.html",
  "search_results": [
    {
      "name": "Kimetsu no Yaiba",
      "url": "https://gogo-stream.com/videos/kimetsu-no-yaiba-episode-26"
    },
    {
      "name": "Kimetsu no Yaiba (Dub)",
      "url": "https://gogo-stream.com/videos/kimetsu-no-yaiba-dub-episode-26"
    }
  ]
}
```

### Show
`GET /show` - Gets the episodes from a show page

Query params:
- `show_url`: String

Example response body:
```
{
  "episodes": [
    {
      "url": "https://gogo-stream.com/videos/kimetsu-no-yaiba-episode-26",
      "ep_num": "26"
    },
    {
      "url": "https://gogo-stream.com/videos/kimetsu-no-yaiba-episode-25",
      "ep_num": "25"
    }
  ]
}
```

### Download Episode
`POST /download/episode` - Downloads episode from episode page

JSON request body:
```
{
	"episode_url" : "https://gogo-stream.com/videos/hajime-no-ippo--episode-20",
	"show_name" : "Hajime_no_Ippo",
	"season" : "1",
	"episode_num" : "20",
	"root_folder" : "/Users/eau/Documents/Test-landing-path/"
}
```

Example response body:
```
{
  "id": "9b982bbc-225c-11eb-9921-34363b742af4"
}
```

### Download from URL
`POST /download/url` - Download a file from the internet, returning the uuid of the download thread

JSON request body:
```
{
	"download_link" : "https://google.com",
	"download_location" : "/Downloads/",
	"file_name" : "test_file.mp4"
}
```

Example response body:
```
{
  "id": "9b982bbc-225c-11eb-9921-34363b742af4"
}
```

### Download Status
`GET /download/status` - Gets the status of the download thread from Redis

Query params:
- `id`: String

Example response body:
```
{
  "download_link": "https://google.com",
  "path": "/Downloads/test_file.mp4",
  "status": "DOWNLOADING",
  "downloaded_bytes": 4718592,
  "total_bytes": 67485201,
  "start_time": 1604906670777,
  "last_update": 1604906735872
}
```

### Get All Download UUIDs
`GET /download/status/all` - Gets the uuids of all download threads

Example response body:
```
{
  "download_ids": [
    "37f05d92-22b0-11eb-a0e3-34363b742af4",
    "3cd89572-22b0-11eb-a0e3-34363b742af4",
    "6e7cd098-22b0-11eb-94ea-34363b742af4"
  ]
}
```

## Running server:
Runs on localhost:9050.

Move service file using
```
sudo cp plex-download-api.service /lib/systemd/system/plex-download-api.service
```

## Redis:
Currently Redis is configured on `localhost:6379`. Installation instructions can be found [here](https://redis.io/topics/quickstart)
