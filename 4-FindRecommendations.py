import sys
import os
from helpers import read_db_from_file


def count_common_elements_by_id(dictionary1, dictionary2, property):
    result = 0
    for first_id in [inner_dictionary1['id'] for inner_dictionary1 in dictionary1[property]]:
        if first_id in [inner_dictionary2['id'] for inner_dictionary2 in dictionary2[property]]:
            result += 1
    return result


def find_movie_by_title(movie_collection, title):

    matching_movies = []
    title = title.lower()

    for movie in movie_collection:
        if movie['title'].lower() == title:
            matching_movies.append(movie)

    if not matching_movies:
        return

    if len(matching_movies) == 1:
        return matching_movies.pop()

    return ask_user_choice(matching_movies)


def ask_user_choice(movie_collection):

    print("Найдено несколько фильмов. Выберете один: ")
    for movie_number, movie in enumerate(movie_collection):
        print("{} - фильм выпущен {}".format(movie_number + 1, movie['release_date']))

    choice = 0
    while choice < 1 or choice > len(movie_collection):
        choice_string = input("Введите номер выбранного фильма: ")
        if choice_string.isdigit():
            choice = int(choice_string)

    return movie_collection[choice - 1]


def get_year_difference(date1, date2):

    days_in_month = 30
    days_in_year = 365

    year1, month1, day1 = [int(date_part) for date_part in date1.split('-')]
    year2, month2, day2 = [int(date_part) for date_part in date2.split('-')]

    days1 = year1 * days_in_year + month1 * days_in_month + day1
    days2 = year2 * days_in_year + month2 * days_in_month + day2

    return abs(days1 - days2) / days_in_year


def find_similarity_coefficient(movie1, movie2):

    number_of_common_keywords = count_common_elements_by_id(movie1, movie2, 'keywords')
    number_of_common_genres = count_common_elements_by_id(movie1, movie2, 'genres')

    is_in_same_collection = movie1['belongs_to_collection'] == \
                            movie2['belongs_to_collection'] or False

    movie_release_date_difference = 0
    if movie1['release_date'] and movie2['release_date']:
        movie_release_date_difference = get_year_difference(movie1['release_date'],
                                                            movie2['release_date'])

    common_production_companies = count_common_elements_by_id(movie1, movie2,
                                                              'production_companies')

    revenue_difference = 0
    revenue1 = int(movie1['revenue'])
    revenue2 = int(movie2['revenue'])
    if  revenue1 and revenue2:
        million = 10000000 # difference of movie revenues is estimated in millions
        revenue_difference = abs(revenue1 - revenue2)/ million

    number_of_common_lists = count_common_elements_by_id(movie1, movie2, 'results')
    number_of_common_casts = count_common_elements_by_id(movie1, movie2, 'cast')
    number_of_common_crews = count_common_elements_by_id(movie1, movie2, 'crew')

    number_of_common_translations = 0
    for translation_code in [translation['iso_639_1'] for translation in movie1['translations']]:
        if translation_code in [translation['iso_639_1'] for translation in movie2['translations']]:
            number_of_common_translations += 1
            
    is_both_movies_adult = movie1['adult'] == movie2['adult']

    return (number_of_common_keywords * 10 + number_of_common_genres * 10 +
            int(is_in_same_collection) * 50 + int(is_both_movies_adult) * 50 +
            -movie_release_date_difference * 5 + common_production_companies * 5 +
            -revenue_difference * 3 + number_of_common_lists * 8 +
            number_of_common_casts * 9 + number_of_common_crews * 9 +
            number_of_common_translations * 8)


def find_interest_coefficient(movie):
    return float(movie['popularity']) * float(movie['vote_average'])


def sort_movies_by_similarity_to_target(target, movie_collection):
    return sorted(all_movies_except_target,
                  key=lambda movie: (find_similarity_coefficient(movie, target),
                                     find_interest_coefficient(movie)),
                  reverse=True)


if __name__ == '__main__':

    db_name = 'database.plat'
    if not os.path.exists(db_name):
        print("Не найдена база данных %s" % db_name)
        sys.exit(1)
    db = read_db_from_file(db_name)

    search_title = input("Введите названия фильма: ")

    target = find_movie_by_title(db, search_title)
    if not target:
        print("Фильм не найден")
        sys.exit(2)

    all_movies_except_target = [movie for movie in db if movie['id'] != target['id']]
    sorted_by_recommendation = sort_movies_by_similarity_to_target(target,
                                                                   all_movies_except_target)

    print("Фильмы, которые вам могут быть интересны: ")
    print("------------------------------------------")
    for movie in sorted_by_recommendation[:10]:
        print("{}, дата выхода - {}".format(movie['title'],
                                            movie.get('release_date', 'неизвестно')))
