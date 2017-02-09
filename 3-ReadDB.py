import json
import sys

def CountFilmsWord(count):
    count %= 10
    if count == 1:
        return 'фильм'
    elif count in range(2, 5):
        return 'фильма'
    else:
        return 'фильмов'

# read db from file
try:
    with open("database.plat") as file_db:
        db = json.load(file_db)
except FileNotFoundError:
    print("Не найдена база данных database.plat")
    sys.exit(0)

if len(db) == 0:
    print("База данных пуста")
    sys.exit(0)

# read string for search
print("Введите строку для поиска названия фильма: ", end = '')
str = input().lower()

found = []
# search
try:
    for movie in db:
        if str in movie['title'].lower():
            found.append(movie)
except (KeyError, TypeError):
    print("База данных повреждена")
    sys.exit(0)

# print results
count = len(found)
if count == 0:
    print("Совпадений не найдено")
else:
    print("Найден{} {} {}: ".format('о' if count % 10 != 1 else '', count, CountFilmsWord(count)))
    for movie in found:
        print(movie['title'])



