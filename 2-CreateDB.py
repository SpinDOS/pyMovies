import random
import urllib
import json
import time
from helpers import make_tmdb_api_request

if __name__ == '__main__':

    db = []
    print("Working.. This operation may take a long time")
    # generate 1000 random numbers of films and download info about them
    for movie_number in random.sample(range(1, 100000) , 1000):

        base_string = '/movie/%d' % movie_number

        # try get info about this movie
        try:
            details = make_tmdb_api_request(base_string)
        except urllib.error.HTTPError as err:
            # if movie with this number is not found - skip this number
            if err.code == 404:
                continue
            else:
                raise

        # get other info
        alternative_titles = make_tmdb_api_request(base_string + '/alternative_titles')
        movie_lists = make_tmdb_api_request(base_string + '/lists')
        movie_keywords = make_tmdb_api_request(base_string + '/keywords')
        movie_credits = make_tmdb_api_request(base_string + '/credits')
        movie_translations = make_tmdb_api_request(base_string + '/translations')

        # rename some properties to make them more informative
        alternative_titles['alternative_titles'] = alternative_titles.pop('titles')
        if movie_lists:
            del movie_lists['page']
            del movie_lists['total_pages']
            movie_lists['lists'] = movie_lists.pop('results')
            movie_lists['total_lists'] = movie_lists.pop('total_results')

        #add to db
        db_entry = {}
        for info_piece in [details, alternative_titles, movie_lists,
                           movie_keywords, movie_credits, movie_translations]:
            db_entry.update(info_piece)

        db.append(db_entry)

    # save db to file
    with open('database.plat', 'w') as outfile:
        json.dump(db, outfile)

    print("Info about %d movies is downloaded and saved to database.plat!" % len(db))