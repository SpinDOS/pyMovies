import urllib.request
import urllib.parse
import json

#number of the movie to find
movie_number = str(215)

#get api key
with open("apikey.json") as file_apikey:
    api_key = json.load(file_apikey)['key']

def load_json_data_from_url(base_url, url_params):
    url = '%s?%s' % (base_url, urllib.parse.urlencode(url_params))
    response = urllib.request.urlopen(url).read().decode('utf-8')
    return json.loads(response)


def make_tmdb_api_request(method, api_key, extra_params=None):
    extra_params = extra_params or {}
    url = 'https://api.themoviedb.org/3%s' % method
    params = {
        'api_key': api_key,
        'language': 'ru',
    }
    params.update(extra_params)
    return load_json_data_from_url(url, params)

movie_info = make_tmdb_api_request(method='/movie/' + movie_number, api_key=api_key)
print(movie_info['budget'])

