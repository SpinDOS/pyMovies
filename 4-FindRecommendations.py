import json
import sys
from datetime import date

def count_common_elements(movie, property):
    result = 0
    for id in [d['id'] for d in target[property]]:
        if id in [d['id'] for d in movie[property]]:
            result += 1
    return result

# find movie by title
def find_target(title):

    # collection of movies with the title
    found = []

    # explore the database
    for movie in db:
        if movie['title'].lower() == title:
            found.append(movie)

    # if title not found
    if len(found) == 0:
        print("Не удалось найти фильм " + title)
        sys.exit(0)

    #if only one movie has this title
    if len(found) == 1:
        return found[0]

    # print info about found movies
    print("Найдено несколько фильмов с данным названием. Выберете один: ")
    for i, movie in enumerate(found):
        print ("{} - фильм выпущен {}".format(i + 1, movie['release_date']))

    # get user's choice
    choice = 0
    while choice < 1 or choice > len(found):
        print("Введите номер выбранного фильма: ", end = '')
        try:
            choice = int(input())
        except ValueError:
            pass

    return found[choice - 1]

# find coefficient of similarit between movie and target
def find_similarity_coefficient(movie):
    # max coefficient for movie itself
    if movie['id'] == target['id']:
        return 1000000000000;
    #find common parts

    keywords = count_common_elements(movie, 'keywords')
    genres = count_common_elements(movie, 'genres')
    collection = 0
    if target['belongs_to_collection'] and movie['belongs_to_collection']:
        if target['belongs_to_collection']['id'] == movie['belongs_to_collection']['id']:
            collection = 1
    release_date = 0
    if target['release_date'] and movie['release_date']:
        y1, m1, d1 = [int(s) for s in target['release_date'].split('-')]
        y2, m2, d2 = [int(s) for s in movie['release_date'].split('-')]
        date1 = y1 * 12 + m1
        date2 = y2 * 12 + m2
        release_date = -abs(date1 - date2) / 12

    production_companies = count_common_elements(movie, 'production_companies')
    revenue = 0
    if target['revenue'] > 0 and movie['revenue'] > 0:
        revenue = -(int(target['revenue']) - int(movie['revenue']))/ 10000000

    lists = count_common_elements(movie, 'lists')
    cast = count_common_elements(movie, 'cast')
    crew = count_common_elements(movie, 'crew')
    

    # find resulting coefficient by summation of multiplication of found numbers and pre-defined importance coefficients
    return keywords * 10 + genres * 10 + collection * 50 + release_date * 5 + production_companies * 5 + revenue * 3 + lists * 8 + cast * 9 + crew * 9



def find_interesting_coefficient(movie):
    return float(movie['popularity']) * float(movie['vote_average'])

# read db from file
try:
    with open("database.plat") as file_db:
        db = json.load(file_db)
except FileNotFoundError:
    print("Не найдена база данных database.plat")
    sys.exit(0)

if len(db) < 2:
    print("База данных пуста или содержит слишком мало элементов")
    sys.exit(0)

# read string for search
print("Введите названия фильма: ", end = '')
str = input().lower()


try:
    # find target movie
    target = find_target(str)

    # get ratings of all movies and sort it
    ratings = [(movie, find_similarity_coefficient(movie)) for movie in db]
    # sort movies by rating
    ratings = sorted(ratings, key = lambda x: (-x[1], -find_interesting_coefficient(x[0])))

    # print best 10 movies
    print("Фильмы, которые вам могут быть интересны: ")
    for movie, r in ratings[1:11]:
        print(movie['title'] + ", дата выхода - " + movie['release_date'])

except (KeyError, TypeError):
    print("База данных повреждена")
    sys.exit(0)


