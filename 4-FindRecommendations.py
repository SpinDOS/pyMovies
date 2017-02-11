import json
import sys
import os

def count_common_elements(dictionary1, dictionary2, property):
    result = 0
    for first_id in [inner_dictionary1['id'] for inner_dictionary1 in dictionary1[property]]:
        if first_id in [inner_dictionary2['id'] for inner_dictionary2 in dictionary2[property]]:
            result += 1
    return result

def find_target(db, title):

    matching_movies = []

    # explore the database
    for movie in db:
        if movie['title'].lower() == title:
            matching_movies.append(movie)

    if not matching_movies:
        print("Не удалось найти фильм %s" % title)
        sys.exit(0)
    if len(matching_movies) == 1:
        return matching_movies.pop()

    # print info about matching movies and select one of them
    print("Найдено несколько фильмов с данным названием. Выберете один: ")
    for movie_number, movie in enumerate(matching_movies):
        print ("{} - фильм выпущен {}".format(movie_number + 1, movie['release_date']))

    # get user's choice
    choice = 0
    while choice < 1 or choice > len(matching_movies):
        try:
            choice = int(input("Введите номер выбранного фильма: "))
        except ValueError:
            pass

    return matching_movies[choice - 1]

def find_similarity_coefficient(movie1, movie2):

    #find common parts

    movie_keywords = count_common_elements(movie1, movie2, 'keywords')
    movie_genres = count_common_elements(movie1, movie2, 'genres')

    movie_collection = 0
    if movie1['belongs_to_collection'] and movie2['belongs_to_collection']:
        if movie1['belongs_to_collection']['id'] == movie2['belongs_to_collection']['id']:
            movie_collection = 1

    movie_release_date = 0
    if movie1['release_date'] and movie2['release_date']:
        y1, m1, d1 = [int(s) for s in movie1['release_date'].split('-')]
        y2, m2, d2 = [int(s) for s in movie2['release_date'].split('-')]
        date1 = y1 * 12 + m1
        date2 = y2 * 12 + m2
        movie_release_date = -abs(date1 - date2) / 12

    movie_production_companies = count_common_elements(movie1, movie2, 'production_companies')

    movie_revenue = 0
    revenue1 = int(movie1['revenue'])
    revenue2 = int(movie2['revenue'])
    if  revenue1> 0 and revenue2 > 0:
        movie_revenue = -abs(revenue1 - revenue2)/ 10000000

    movie_lists = count_common_elements(movie1, movie2, 'lists')
    movie_cast = count_common_elements(movie1, movie2, 'cast')
    movie_crew = count_common_elements(movie1, movie2, 'crew')

    movie_translations = 0
    for translation_code in [translation['iso_639_1'] for translation in movie1['translations']]:
        if translation_code in [translation['iso_639_1'] for translation in movie2['translations']]:
            movie_translations += 1

    if movie1['adult'] == movie2['adult']:
        movie_adult = 1
    else:
        movie_adult = 0

    # find resulting coefficient by summation of multiplication of
    # found numbers and pre-defined importance coefficients
    return (movie_keywords * 10 + movie_genres * 10 + movie_collection * 50 + movie_adult * 50 +
            movie_release_date * 5 + movie_production_companies * 5 + movie_revenue * 3 +
            movie_lists * 8 + movie_cast * 9 + movie_crew * 9 + movie_translations * 8)


def find_interestingness_coefficient(movie):
    return float(movie['popularity']) * float(movie['vote_average'])

if __name__ == '__main__':

    # read db from file
    database_path = 'database.plat'
    if not os.path.exists(database_path):
        print("Не найдена база данных database.plat")
        sys.exit(0)

    with open(database_path, 'r') as file_db:
            db = json.load(file_db)

    if len(db) < 2:
        print("База данных пуста или содержит слишком мало элементов")
        sys.exit(0)

    search_title = input("Введите названия фильма: ").lower()
    try:
        target = find_target(db, search_title)

        sorted_by_recommendation = sorted([movie for movie in db if movie['id'] != target['id']],
            key = lambda m: (find_similarity_coefficient(m, target),
                             find_interestingness_coefficient(m)),
            reverse = True)

        # print best 10 movies
        print("Фильмы, которые вам могут быть интересны: ")
        print("------------------------------------------")
        for movie in sorted_by_recommendation[:10]:
            print("{}, дата выхода - {}".format(movie['title'], movie['release_date'] or 'неизвестно'))

    except (KeyError, TypeError):
        print("База данных повреждена")
        sys.exit(0)


