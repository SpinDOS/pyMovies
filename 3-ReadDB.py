import json
import sys
import os
from helpers import read_db_from_file


def find_movies_by_title_part(movies_collection, part_of_title_to_search):
    matching_movies = []
    part_of_title_to_search = part_of_title_to_search.lower()

    for movie in movies_collection:
        title = movie['title']
        if part_of_title_to_search in title.lower():
            matching_movies.append(movie)

    return matching_movies


def print_found_movies(collection_of_found_movies):

    found_movies_count = len(matching_movies)
    if not found_movies_count:
        print("Фильмы не найдены")
        return None

    count_last_digit = found_movies_count % 10
    print("Найден{} {} фильм{}: ".format('о' if count_last_digit != 1 else '',
                                         found_movies_count,
                                         ('' if count_last_digit == 1 else
                                          'а' if count_last_digit in range(2, 5) else
                                          'ов')))
    for movie in collection_of_found_movies:
        print(movie['title'])


if __name__ == '__main__':

    try:
        db = read_db_from_file()
    except FileNotFoundError:
        print("Не найдена база данных database.plat")
        sys.exit(1)

    search_string = input("Введите строку для поиска названия фильма: ").lower()

    try:
        matching_movies = find_movies_by_title_part(db, search_string)
    except (KeyError, TypeError):
        print("База данных повреждена")
        sys.exit(2)

    print_found_movies(matching_movies)



