import random
import urllib
import json
from lib import make_tmdb_api_request

db = []
nums = set()

print("Working.. This operation may take a long time")
# generate 1000 random numbers of films and download info about them
while len(nums) != 1000:
    # generate unique number of movie
    n = random.randint(1, 100000)
    while n in nums:
        n = random.randint(1, 100000)

    base_string = '/movie/' + str(n)

    # try get info about this movie
    try:
        details = make_tmdb_api_request(base_string)
    except urllib.error.HTTPError as err:
        # if movie with this number is not found - generate new number
        if err.code == 404:
            continue
        else:
            raise
    # if the movie is found
    nums.add(n)
    # get another info
    alternative_titles = make_tmdb_api_request(base_string + '/alternative_titles')
    lists = make_tmdb_api_request(base_string + '/lists')
    keywords = make_tmdb_api_request(base_string + '/keywords')
    movie_credits = make_tmdb_api_request(base_string + '/credits')

    # delete useless info
    details.pop('backdrop_path')
    if details['belongs_to_collection'] != None:
        details['belongs_to_collection'].pop('poster_path')
        details['belongs_to_collection'].pop('backdrop_path')
    details.pop('homepage')
    details.pop('imdb_id')
    details.pop('poster_path')
    details.pop('runtime')
    details.pop('tagline')
    details.pop('video')

    if lists != None:
        lists.pop('page')
        lists.pop('total_pages')
        if lists['results'] != None:
            for res in lists['results']:
                res.pop('poster_path')

    if movie_credits != None:
        if movie_credits['cast'] != None:
            for cast in movie_credits['cast']:
                cast.pop('profile_path')
        if movie_credits['crew'] != None:
            for cast in movie_credits['crew']:
                cast.pop('profile_path')

    #add to db
    db_entry = {}
    db_entry.update(details)
    db_entry.update(alternative_titles)
    db_entry.update(lists)
    db_entry.update(keywords)
    db_entry.update(movie_credits)
    db_entry['id'] = len(nums)
    db.append(db_entry)

# save db to file
with open('database.plat', 'w') as outfile:
    json.dump(db, outfile)

print("Info about 1000 movies is downloaded and saved to database.plat!")