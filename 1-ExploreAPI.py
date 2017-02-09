from lib import make_tmdb_api_request

#number of the movie to find
movie_number = str(215)

movie_info = make_tmdb_api_request(method='/movie/' + movie_number)
print(movie_info['budget'])

