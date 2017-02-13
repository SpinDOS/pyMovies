import urllib.request
import urllib.parse
import json
import time
import sys

#get api key
api_key_path = 'apikey.json'
try:
    with open(api_key_path, 'r') as file_apikey:
        api_key = json.load(file_apikey)['key']
except (FileNotFoundError, TypeError, KeyError, json.decoder.JSONDecodeError):
    print("Пожалуйста, поместите токен TMDB в файл %s" % api_key_path)
    sys.exit(0)

def load_json_data_from_url(base_url, url_params):
    url = '%s?%s' % (base_url, urllib.parse.urlencode(url_params))
    try:
        response = urllib.request.urlopen(url).read().decode('utf-8')
    except urllib.error.HTTPError as err:
        if err.code == 401:
            print("Неверный токен TMDB: %s" % api_key)
            sys.exit(0)
        # tmdb api limit - 40 requests per 10 sec causes 429 code error
        if err.code == 429:
            time.sleep(10) 
            return load_json_data_from_url(base_url, url_params)
        else:
            raise
    return json.loads(response)


def make_tmdb_api_request(method, extra_params=None):
    extra_params = extra_params or {}
    url = 'https://api.themoviedb.org/3%s' % method
    params = {
        'api_key': api_key,
        'language': 'ru',
    }
    params.update(extra_params)
    return load_json_data_from_url(url, params)


def save_db_to_file(db, output_name='database.plat'):
    with open(output_name, 'w') as outfile:
        json.dump(db, outfile)


def read_db_from_file(database_path='database.plat'):
    with open(database_path, 'r') as file_db:
        return json.load(file_db)