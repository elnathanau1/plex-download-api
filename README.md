# plex-download-api
API written to download media from the web for Plex server

## API Spec
### Search
`/search` - Hits search endpoint of api source.

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



## Running server:
Runs on localhost:9050.

Move service file using
```
sudo cp plex-download-api.service /lib/systemd/system/plex-download-api.service
```
