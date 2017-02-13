import random
import urllib
import json
import time
import helpers


def get_random_movies_info(list_of_info_keys = [], number_of_samples=1000):
    movies_list = []
    for movie_number in random.sample(range(1, 100000) , number_of_samples):

        base_string = '/movie/%d' % movie_number
        try:
            movie_info = helpers.make_tmdb_api_request(base_string)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                continue
            else:
                raise

        for info_key in list_of_info_keys:
            movie_info_piece = helpers.make_tmdb_api_request('{}/{}'.format(base_string, info_key))
            movie_info.update(movie_info_piece)

        movies_list.append(movie_info)

    return movies_list


if __name__ == '__main__':

    print("Working.. This operation may take a long time")
    list_of_info_keys = ['alternative_titles', 'lists', 'keywords', 'credits', 'translations']
    db = get_random_movies_info(list_of_info_keys)
    helpers.save_db_to_file(db)
    print("Info about %d movies is downloaded and saved to database.plat!" % len(db))