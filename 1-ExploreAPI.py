from helpers import make_tmdb_api_request

#number of the movie to find
movie_number = 215

movie_info = make_tmdb_api_request('/movie/%d' % movie_number)
print(movie_info['budget'])

