import json
import sys
import os

# read db from file
database_path = 'database.plat'
if not os.path.exists(database_path):
    print("Не найдена база данных database.plat")
    sys.exit(0)

with open(database_path, 'r') as file_db:
        db = json.load(file_db)
if not db:
    print("База данных пуста")
    sys.exit(0)

# search
search_string = input("Введите строку для поиска названия фильма: ").lower()
matching_movies = []
for movie in db:
    title = movie.get('title')
    if title is None or not isinstance(title, str):
        print("База данных повреждена")
        sys.exit(0)
    if search_string in title.lower():
            matching_movies.append(movie)


# print results
matching_movies_count = len(matching_movies)
if not matching_movies_count:
    print("Совпадений не найдено")
else:
    count_last_digit = matching_movies_count % 10
    print("Найден{} {} фильм{}: ".format('о' if count_last_digit != 1 else '',
                                         matching_movies_count,
                                         ('f' if count_last_digit == 1 else
                                          'а' if count_last_digit in range(2, 5) else
                                          'ов')))
    for movie in matching_movies:
        print(movie['title'])



